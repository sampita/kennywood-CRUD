"""View module for handling requests about intineraries"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction, ParkArea, Itinerary, Customer

class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for intineraries

    Arguments:
        serializers
    """

    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction',)
        depth = 2

class ItineraryItems(ViewSet):
    """Itinerary items for Kennywood Amusement Park"""

    # Handles POST
    def create(self, request):
        new_itinerary_item = Itinerary()
        new_itinerary_item.starttime = request.data["starttime"]
        new_itinerary_item.customer_id = request.auth.user.customer.id
        new_itinerary_item.attraction_id = request.data["ride_id"]

        new_itinerary_item.save()

        serializer = ItinerarySerializer(new_itinerary_item, context={'request': request})

        return Response(serializer.data)
    
    # handles GET one ( the /<some_number tells it that)
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single itinerary item

        Returns:
            Response -- JSON serialized itinerary instance
        """
        try:
            itinerary_item = Itinerary.objects.get(pk=pk)
            serializer = ItinerarySerializer(itinerary_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    # handles GET all
    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        areas = Itinerary.objects.all()
        serializer = ItinerarySerializer(
            areas,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    # handles PUT
    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        new_itinerary_item = Itinerary.objects.get(pk=pk)
        new_itinerary_item.starttime = request.data["starttime"]
        new_itinerary_item.customer_id = request.auth.user.customer.id
        new_itinerary_item.attraction_id = request.data["ride_id"]
        new_itinerary_item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    # handles DELETE
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park area

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            area = Itinerary.objects.get(pk=pk)
            area.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

