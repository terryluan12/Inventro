from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Item
from inventory.models import InventoryItem

@api_view(["GET"])
def api_search(request):
    """
    Simple search endpoint used by the frontend quick-search.
    GET /api/search/?q=term
    """
    q = (request.GET.get("q") or "").strip()
    results = {"items": [], "inventory": []}
    if q:
        results["items"] = list(
            Item.objects.filter(name__icontains=q).values("id", "name", "SKU")[:10]
        )
        results["inventory"] = list(
            InventoryItem.objects.filter(name__icontains=q).values(
                "id", "name", "category", "location"
            )[:10]
        )
    return Response(results)
