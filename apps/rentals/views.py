from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect

from rentals.models import Rental


# AJAX requests -- TODO there is currently NO SECURITY on these AJAX calls

@login_required
def remove_rental(request, rental_id=None):
    """Remove rental from dashboard.

       Now this view just removes the rental from your agency's list of approved
       rentals. do we want this to be on a per-user basis?
       we should just remove it from THAT
       user's view. Yay more model fields.  TODO: (for project grepping)"""
    try:
        print "TRY!"
        rental = Rental.objects.get(id=rental_id)
        print request.user
        # TODO: this is a janky workaround for brokers to be able
        # to remove rentals from their agency list AND allow agency
        # heads to remove (case of a 1 man agency).  should just force
        # agency heads to belong to their own agency as a broker as well.
        # this will be implemented when a better registration procedure exists
        #
        print request.user.broker.agency
        if request.user.broker.agency:
            agency = request.user.broker.agency
        else:
            agency = request.user.agency
        print agency.rentals.all().count()
        agency.rentals.remove(rental)
        print agency.rentals.all().count()
    except:
        return HttpResponse("Fail")
    else:
        return HttpResponse("Success")
