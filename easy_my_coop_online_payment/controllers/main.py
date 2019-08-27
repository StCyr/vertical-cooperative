# -*- coding: utf-8 -*-

from openerp import http
from openerp.http import request
from openerp.tools.translate import _

from openerp.addons.easy_my_coop.controllers.main import WebsiteSubscription
from openerp.addons.website_payment.controllers.main import website_payment


class SubscriptionOnlinePayment(WebsiteSubscription):

    def fill_values(self, values, is_company, load_from_user=False):
        values = super(SubscriptionOnlinePayment, self).fill_values(values, is_company, load_from_user)
        fields_desc = request.env['subscription.request'].sudo().fields_get(['payment_type'])
        values['payment_types'] = fields_desc['payment_type']['selection']

        return values

    def get_subscription_response(self, values, kwargs):
        subscription = values.get('subscription_id', False)
        if kwargs.get('payment_type') == 'online':
            invoice = subscription.validate_subscription_request()[0]
            acquirer = request.env['payment.acquirer'].search([('website_published', '=', True)])[0]
            return website_payment().pay(reference=invoice.number, amount=invoice.residual, currency_id=invoice.currency_id.id, acquirer_id=acquirer.id)
        else:
            values = self.preRenderThanks(values, kwargs)
            return request.website.render(kwargs.get("view_callback", "easy_my_coop.cooperator_thanks"), values)

        return True


class SubscriptionWebsitePayment(website_payment):

    @http.route(['/website_payment/transaction'],
                type='json',
                auth="public", website=True)
    def transaction(self, reference, amount, currency_id, acquirer_id):
        inv_obj = request.env['account.invoice']
        partner_id = request.env.user.partner_id.id if request.env.user.partner_id != request.website.partner_id else False
        capital_release_request = inv_obj.sudo().search([('release_capital_request', '=', True),
                                                         ('number', '=', reference)])

        values = {
            'acquirer_id': int(acquirer_id),
            'reference': reference,
            'amount': float(amount),
            'currency_id': int(currency_id),
            'partner_id': partner_id,
        }

        if len(capital_release_request) > 0:
            values['partner_id'] = capital_release_request.partner_id.id
            values['release_capital_request'] = capital_release_request.id

        tx = request.env['payment.transaction'].sudo().create(values)
        request.session['website_payment_tx_id'] = tx.id
        return tx.id

    @http.route(['/website_payment/confirm'],
                type='http',
                auth='public', website=True)
    def confirm(self, **kw):
        tx_id = request.session.pop('website_payment_tx_id', False)
        if tx_id:
            tx = request.env['payment.transaction'].sudo().browse(tx_id)
            status = (tx.state == 'done' and 'success') or 'danger'
            message = (tx.state == 'done' and 'Your payment was successful! It may take some time to be validated on our end.') or 'OOps! There was a problem with your payment.'
            return request.website.render('website_payment.confirm', {'tx': tx, 'status': status, 'message': message})
        else:
            return request.redirect('/my/home')

    @http.route(['/website_payment/pay'],
                type='http',
                auth='public', website=True)
    def pay(self, reference='', amount=False, currency_id=None,
            acquirer_id=None, **kw):
        env = request.env
        user = env.user.sudo()

        currency_id = currency_id and int(currency_id) or user.company_id.currency_id.id
        currency = env['res.currency'].browse(currency_id)

        # Try default one then fallback on first
        acquirer_id = acquirer_id and int(acquirer_id) or \
            env['ir.values'].get_default('payment.transaction', 'acquirer_id', company_id=user.company_id.id) or \
            env['payment.acquirer'].search([('website_published', '=', True), ('company_id', '=', user.company_id.id)])[0].id

        acquirer = env['payment.acquirer'].with_context(submit_class='btn btn-primary pull-right',
                                                        submit_txt=_('Pay Now')).browse(acquirer_id)
        # auto-increment reference with a number suffix if the reference already exists
        reference = request.env['payment.transaction'].get_next_reference(reference)

        partner_id = user.partner_id.id if user.partner_id.id != request.website.partner_id.id else False
        capital_release_request = request.env['account.invoice'].sudo().search(
                                    [('release_capital_request', '=', True),
                                     ('number', '=', reference)]
                                    )

        if len(capital_release_request) > 0:
            partner_id = capital_release_request.partner_id.id

        payment_form = acquirer.sudo().render(reference, float(amount), currency.id, values={'return_url': '/website_payment/confirm', 'partner_id': partner_id})[0]
        values = {
            'reference': reference,
            'acquirer': acquirer,
            'currency': currency,
            'amount': float(amount),
            'payment_form': payment_form,
        }
        return request.website.render('website_payment.pay', values)
