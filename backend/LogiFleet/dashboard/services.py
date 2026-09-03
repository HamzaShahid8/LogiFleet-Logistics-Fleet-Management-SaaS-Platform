from decimal import Decimal

from django.db.models import Count, Sum, Q

from accounts.models import User
from roles_permissions.models import Roles, Permissions
from customer_management.models import Customer
from driver_management.models import Driver
from vehicle_management.models import Vehicle
from shipping_management.models import Shipment
from expense_management.models import Expense
from invoice_management.models import Invoice
from payment_management.models import Payment


class DashboardService:

    @staticmethod
    def get_superuser_dashboard(user):

        users = User.objects.aggregate(
            total=Count('id'),
            verified=Count(
                'id',
                filter=Q(is_email_verified=True)
            ),
        )

        customers = Customer.objects.count()
        drivers = Driver.objects.count()
        vehicles = Vehicle.objects.count()

        shipments = Shipment.objects.aggregate(
            total=Count('id'),
            pending=Count(
                'id',
                filter=Q(status='pending')
            ),
            assigned=Count(
                'id',
                filter=Q(status='assigned')
            ),
            picked_up=Count(
                'id',
                filter=Q(status='picked_up')
            ),
            in_transit=Count(
                'id',
                filter=Q(status='in_transit')
            ),
            out_for_delivery=Count(
                'id',
                filter=Q(status='out_for_delivery')
            ),
            delivered=Count(
                'id',
                filter=Q(status='delivered')
            ),
            failed=Count(
                'id',
                filter=Q(status='failed')
            ),
            cancelled=Count(
                'id',
                filter=Q(status='cancelled')
            ),
        )

        invoices = Invoice.objects.aggregate(
            total=Count('id'),
            total_amount=Sum('total_amount'),
            paid_amount=Sum('paid_amount'),
            draft=Count(
                'id',
                filter=Q(status='draft')
            ),
            issued=Count(
                'id',
                filter=Q(status='issued')
            ),
            partially_paid=Count(
                'id',
                filter=Q(status='partially_paid')
            ),
            paid=Count(
                'id',
                filter=Q(status='paid')
            ),
            overdue=Count(
                'id',
                filter=Q(status='overdue')
            ),
            cancelled=Count(
                'id',
                filter=Q(status='cancelled')
            ),
        )

        payments = Payment.objects.aggregate(
            total=Count('id'),
            completed=Count(
                'id',
                filter=Q(status='completed')
            ),
            pending=Count(
                'id',
                filter=Q(status='pending')
            ),
            failed=Count(
                'id',
                filter=Q(status='failed')
            ),
            cancelled=Count(
                'id',
                filter=Q(status='cancelled')
            ),
            total_received=Sum(
                'amount',
                filter=Q(status='completed')
            ),
        )

        expenses = Expense.objects.aggregate(
            total=Count('id'),
            total_amount=Sum('amount'),
        )

        total_invoice = (
            invoices['total_amount']
            or Decimal('0.00')
        )

        paid_amount = (
            invoices['paid_amount']
            or Decimal('0.00')
        )

        total_received = (
            payments['total_received']
            or Decimal('0.00')
        )

        total_expenses = (
            expenses['total_amount']
            or Decimal('0.00')
        )

        outstanding = total_invoice - paid_amount
        net = total_received - total_expenses

        total_shipments = shipments['total'] or 0
        delivered = shipments['delivered'] or 0

        delivery_rate = (
            (delivered / total_shipments) * 100
            if total_shipments
            else 0
        )

        return {
            'role': 'Superuser',

            'users': {
                'total': users['total'],
                'verified_emails': users['verified'],
            },

            'resources': {
                'customers': customers,
                'drivers': drivers,
                'vehicles': vehicles,
            },

            'shipments': {
                'total': total_shipments,
                'pending': shipments['pending'],
                'assigned': shipments['assigned'],
                'picked_up': shipments['picked_up'],
                'in_transit': shipments['in_transit'],
                'out_for_delivery': shipments['out_for_delivery'],
                'delivered': delivered,
                'failed': shipments['failed'],
                'cancelled': shipments['cancelled'],
                'delivery_rate': round(
                    delivery_rate,
                    2
                ),
            },

            'invoices': {
                'total': invoices['total'],
                'total_amount': str(total_invoice),
                'paid_amount': str(paid_amount),
                'outstanding': str(outstanding),

                'draft': invoices['draft'],
                'issued': invoices['issued'],
                'partially_paid': invoices['partially_paid'],
                'paid': invoices['paid'],
                'overdue': invoices['overdue'],
                'cancelled': invoices['cancelled'],
            },

            'payments': {
                'total': payments['total'],
                'completed': payments['completed'],
                'pending': payments['pending'],
                'failed': payments['failed'],
                'cancelled': payments['cancelled'],
                'total_received': str(total_received),
            },

            'expenses': {
                'total': expenses['total'],
                'total_amount': str(total_expenses),
            },

            'financial_summary': {
                'revenue': str(total_received),
                'expenses': str(total_expenses),
                'net': str(net),
                'outstanding': str(outstanding),
            },
        }

    @staticmethod
    def get_data(user):

        # SUPERUSER
        if user.is_superuser:

            return DashboardService.get_superuser_dashboard(user)

        # COMPANY ADMIN
        elif user.role and user.role.name == 'Company_Admin':

            users = User.objects.aggregate(
                total=Count('id'),
                verified=Count(
                    'id',
                    filter=Q(is_email_verified=True)
                ),
            )

            customers = Customer.objects.count()
            drivers = Driver.objects.count()
            vehicles = Vehicle.objects.count()

            shipments = Shipment.objects.aggregate(
                total=Count('id'),
                pending=Count(
                    'id',
                    filter=Q(status='pending')
                ),
                assigned=Count(
                    'id',
                    filter=Q(status='assigned')
                ),
                picked_up=Count(
                    'id',
                    filter=Q(status='picked_up')
                ),
                in_transit=Count(
                    'id',
                    filter=Q(status='in_transit')
                ),
                out_for_delivery=Count(
                    'id',
                    filter=Q(status='out_for_delivery')
                ),
                delivered=Count(
                    'id',
                    filter=Q(status='delivered')
                ),
                failed=Count(
                    'id',
                    filter=Q(status='failed')
                ),
                cancelled=Count(
                    'id',
                    filter=Q(status='cancelled')
                ),
            )

            invoices = Invoice.objects.aggregate(
                total=Count('id'),
                total_amount=Sum('total_amount'),
                paid_amount=Sum('paid_amount'),
                draft=Count(
                    'id',
                    filter=Q(status='draft')
                ),
                issued=Count(
                    'id',
                    filter=Q(status='issued')
                ),
                partially_paid=Count(
                    'id',
                    filter=Q(status='partially_paid')
                ),
                paid=Count(
                    'id',
                    filter=Q(status='paid')
                ),
                overdue=Count(
                    'id',
                    filter=Q(status='overdue')
                ),
                cancelled=Count(
                    'id',
                    filter=Q(status='cancelled')
                ),
            )

            payments = Payment.objects.aggregate(
                total=Count('id'),
                completed=Count(
                    'id',
                    filter=Q(status='completed')
                ),
                pending=Count(
                    'id',
                    filter=Q(status='pending')
                ),
                failed=Count(
                    'id',
                    filter=Q(status='failed')
                ),
                cancelled=Count(
                    'id',
                    filter=Q(status='cancelled')
                ),
                total_received=Sum(
                    'amount',
                    filter=Q(status='completed')
                ),
            )

            expenses = Expense.objects.aggregate(
                total=Count('id'),
                total_amount=Sum('amount'),
            )

            total_invoice = (
                invoices['total_amount']
                or Decimal('0.00')
            )

            paid_amount = (
                invoices['paid_amount']
                or Decimal('0.00')
            )

            total_received = (
                payments['total_received']
                or Decimal('0.00')
            )

            total_expenses = (
                expenses['total_amount']
                or Decimal('0.00')
            )

            outstanding = total_invoice - paid_amount
            net = total_received - total_expenses

            total_shipments = shipments['total'] or 0
            delivered = shipments['delivered'] or 0

            delivery_rate = (
                (delivered / total_shipments) * 100
                if total_shipments
                else 0
            )

            return {
                'role': user.role.name,

                'users': {
                    'total': users['total'],
                    'verified_emails': users['verified'],
                },

                'resources': {
                    'customers': customers,
                    'drivers': drivers,
                    'vehicles': vehicles,
                },

                'shipments': {
                    'total': total_shipments,
                    'pending': shipments['pending'],
                    'assigned': shipments['assigned'],
                    'picked_up': shipments['picked_up'],
                    'in_transit': shipments['in_transit'],
                    'out_for_delivery': shipments['out_for_delivery'],
                    'delivered': delivered,
                    'failed': shipments['failed'],
                    'cancelled': shipments['cancelled'],
                    'delivery_rate': round(
                        delivery_rate,
                        2
                    ),
                },

                'invoices': {
                    'total': invoices['total'],
                    'total_amount': str(total_invoice),
                    'paid_amount': str(paid_amount),
                    'outstanding': str(outstanding),
                    'draft': invoices['draft'],
                    'issued': invoices['issued'],
                    'partially_paid': invoices['partially_paid'],
                    'paid': invoices['paid'],
                    'overdue': invoices['overdue'],
                    'cancelled': invoices['cancelled'],
                },

                'payments': {
                    'total': payments['total'],
                    'completed': payments['completed'],
                    'pending': payments['pending'],
                    'failed': payments['failed'],
                    'cancelled': payments['cancelled'],
                    'total_received': str(total_received),
                },

                'expenses': {
                    'total': expenses['total'],
                    'total_amount': str(total_expenses),
                },

                'financial_summary': {
                    'revenue': str(total_received),
                    'expenses': str(total_expenses),
                    'net': str(net),
                    'outstanding': str(outstanding),
                },
            }

        # OPERATIONS MANAGER
        elif user.role and user.role.name == 'Operations_Manager':

            customers = Customer.objects.count()
            drivers = Driver.objects.count()

            shipments = Shipment.objects.aggregate(
                total=Count('id'),
                pending=Count(
                    'id',
                    filter=Q(status='pending')
                ),
                assigned=Count(
                    'id',
                    filter=Q(status='assigned')
                ),
                picked_up=Count(
                    'id',
                    filter=Q(status='picked_up')
                ),
                in_transit=Count(
                    'id',
                    filter=Q(status='in_transit')
                ),
                out_for_delivery=Count(
                    'id',
                    filter=Q(status='out_for_delivery')
                ),
                delivered=Count(
                    'id',
                    filter=Q(status='delivered')
                ),
                failed=Count(
                    'id',
                    filter=Q(status='failed')
                ),
                cancelled=Count(
                    'id',
                    filter=Q(status='cancelled')
                ),
            )

            total_shipments = shipments['total'] or 0
            delivered = shipments['delivered'] or 0

            delivery_rate = (
                (delivered / total_shipments) * 100
                if total_shipments
                else 0
            )

            return {
                'role': user.role.name,

                'operations': {
                    'customers': customers,
                    'drivers': drivers,
                },

                'shipments': {
                    'total': total_shipments,
                    'pending': shipments['pending'],
                    'assigned': shipments['assigned'],
                    'picked_up': shipments['picked_up'],
                    'in_transit': shipments['in_transit'],
                    'out_for_delivery': shipments['out_for_delivery'],
                    'delivered': delivered,
                    'failed': shipments['failed'],
                    'cancelled': shipments['cancelled'],
                    'delivery_rate': round(
                        delivery_rate,
                        2
                    ),
                },
            }

        # FLEET MANAGER
        elif user.role and user.role.name == 'Fleet_Manager':

            vehicles = Vehicle.objects.aggregate(
                total=Count('id'),
                available=Count(
                    'id',
                    filter=Q(status='available')
                ),
                assigned=Count(
                    'id',
                    filter=Q(status='assigned')
                ),
                maintenance=Count(
                    'id',
                    filter=Q(status='maintenance')
                ),
                inactive=Count(
                    'id',
                    filter=Q(status='inactive')
                ),
                retired=Count(
                    'id',
                    filter=Q(status='retired')
                ),
            )

            drivers = Driver.objects.aggregate(
                total=Count('id'),
                active=Count(
                    'id',
                    filter=Q(status='active')
                ),
                resigned=Count(
                    'id',
                    filter=Q(status='resigned')
                ),
                fire=Count(
                    'id',
                    filter=Q(status='fire')
                ),
            )

            shipments = Shipment.objects.aggregate(
                total=Count('id'),
                assigned=Count(
                    'id',
                    filter=Q(status='assigned')
                ),
                picked_up=Count(
                    'id',
                    filter=Q(status='picked_up')
                ),
                in_transit=Count(
                    'id',
                    filter=Q(status='in_transit')
                ),
                out_for_delivery=Count(
                    'id',
                    filter=Q(status='out_for_delivery')
                ),
                delivered=Count(
                    'id',
                    filter=Q(status='delivered')
                ),
                failed=Count(
                    'id',
                    filter=Q(status='failed')
                ),
                cancelled=Count(
                    'id',
                    filter=Q(status='cancelled')
                ),
            )

            return {
                'role': user.role.name,

                'vehicles': {
                    'total': vehicles['total'],
                    'available': vehicles['available'],
                    'assigned': vehicles['assigned'],
                    'maintenance': vehicles['maintenance'],
                    'inactive': vehicles['inactive'],
                    'retired': vehicles['retired'],
                },

                'drivers': {
                    'total': drivers['total'],
                    'active': drivers['active'],
                    'resigned': drivers['resigned'],
                    'fire': drivers['fire'],
                },

                'shipments': {
                    'total': shipments['total'],
                    'assigned': shipments['assigned'],
                    'picked_up': shipments['picked_up'],
                    'in_transit': shipments['in_transit'],
                    'out_for_delivery': shipments['out_for_delivery'],
                    'delivered': shipments['delivered'],
                    'failed': shipments['failed'],
                    'cancelled': shipments['cancelled'],
                },
            }

        # ACCOUNTANT
        elif user.role and user.role.name == 'Accountant':

            invoices = Invoice.objects.aggregate(
                total=Count('id'),
                total_amount=Sum('total_amount'),
                paid_amount=Sum('paid_amount'),
                draft=Count(
                    'id',
                    filter=Q(status='draft')
                ),
                issued=Count(
                    'id',
                    filter=Q(status='issued')
                ),
                partially_paid=Count(
                    'id',
                    filter=Q(status='partially_paid')
                ),
                paid=Count(
                    'id',
                    filter=Q(status='paid')
                ),
                overdue=Count(
                    'id',
                    filter=Q(status='overdue')
                ),
                cancelled=Count(
                    'id',
                    filter=Q(status='cancelled')
                ),
            )

            payments = Payment.objects.aggregate(
                total=Count('id'),
                completed=Count(
                    'id',
                    filter=Q(status='completed')
                ),
                pending=Count(
                    'id',
                    filter=Q(status='pending')
                ),
                failed=Count(
                    'id',
                    filter=Q(status='failed')
                ),
                cancelled=Count(
                    'id',
                    filter=Q(status='cancelled')
                ),
                total_received=Sum(
                    'amount',
                    filter=Q(status='completed')
                ),
            )

            expenses = Expense.objects.aggregate(
                total=Count('id'),
                total_amount=Sum('amount'),
            )

            total_invoice = (
                invoices['total_amount']
                or Decimal('0.00')
            )

            paid_amount = (
                invoices['paid_amount']
                or Decimal('0.00')
            )

            total_received = (
                payments['total_received']
                or Decimal('0.00')
            )

            total_expenses = (
                expenses['total_amount']
                or Decimal('0.00')
            )

            outstanding = total_invoice - paid_amount
            net = total_received - total_expenses

            return {
                'role': user.role.name,

                'invoices': {
                    'total': invoices['total'],
                    'total_amount': str(total_invoice),
                    'paid_amount': str(paid_amount),
                    'outstanding': str(outstanding),
                    'draft': invoices['draft'],
                    'issued': invoices['issued'],
                    'partially_paid': invoices['partially_paid'],
                    'paid': invoices['paid'],
                    'overdue': invoices['overdue'],
                    'cancelled': invoices['cancelled'],
                },

                'payments': {
                    'total': payments['total'],
                    'completed': payments['completed'],
                    'pending': payments['pending'],
                    'failed': payments['failed'],
                    'cancelled': payments['cancelled'],
                    'total_received': str(total_received),
                },

                'expenses': {
                    'total': expenses['total'],
                    'total_amount': str(total_expenses),
                },

                'financial_summary': {
                    'revenue': str(total_received),
                    'expenses': str(total_expenses),
                    'net': str(net),
                    'outstanding': str(outstanding),
                },
            }

        # DISPATCHER
        elif user.role and user.role.name == 'Dispatcher':

            shipments = Shipment.objects.aggregate(
                total=Count('id'),
                pending=Count(
                    'id',
                    filter=Q(status='pending')
                ),
                assigned=Count(
                    'id',
                    filter=Q(status='assigned')
                ),
                picked_up=Count(
                    'id',
                    filter=Q(status='picked_up')
                ),
                in_transit=Count(
                    'id',
                    filter=Q(status='in_transit')
                ),
                out_for_delivery=Count(
                    'id',
                    filter=Q(status='out_for_delivery')
                ),
                delivered=Count(
                    'id',
                    filter=Q(status='delivered')
                ),
                failed=Count(
                    'id',
                    filter=Q(status='failed')
                ),
                cancelled=Count(
                    'id',
                    filter=Q(status='cancelled')
                ),
            )

            drivers = Driver.objects.count()
            vehicles = Vehicle.objects.count()

            return {
                'role': user.role.name,

                'shipments': {
                    'total': shipments['total'],
                    'pending': shipments['pending'],
                    'assigned': shipments['assigned'],
                    'picked_up': shipments['picked_up'],
                    'in_transit': shipments['in_transit'],
                    'out_for_delivery': shipments['out_for_delivery'],
                    'delivered': shipments['delivered'],
                    'failed': shipments['failed'],
                    'cancelled': shipments['cancelled'],
                },

                'resources': {
                    'drivers': drivers,
                    'vehicles': vehicles,
                },
            }

        # DRIVER
        elif user.role and user.role.name == 'Driver':

            return {
                'role': user.role.name,
                'message': (
                    'Driver dashboard requires a relation '
                    'between Driver and User.'
                ),
            }

        # UNKNOWN ROLE
        else:

            return {
                'message': 'Unknown role.'
            }