from django.contrib.auth.hashers import check_password
from rest_framework import viewsets
from .models import Property,UserTable,TenentRentAggriment,Units
from .serializers import PropertySerializer,UserTableSerializer,TenentRentAggrimentSerializer,UnitSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import date
from django.http import Http404
import time


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        email=request.data.get('email')



        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'This username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)


class SignInView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': 'User authenticated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class UserTableView(APIView):
    def post(self, request):
        serializer = UserTableSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = UserTable.objects.filter(email=email).first()
        except UserTable.DoesNotExist:
            return Response('User does not exist', status=status.HTTP_404_NOT_FOUND)
        if check_password(password, user.password):
            return Response({"user_id": user.user_id}, status=status.HTTP_200_OK)
        else:
            return Response('Invalid credentials', status=status.HTTP_401_UNAUTHORIZED)

class Userinfo(APIView):

    def get(self, request, user_id):
        try:
            user_data = UserTable.objects.get(user_id=user_id)
            serializer = UserTableSerializer(user_data)
            return Response({'user_details': serializer.data})
        except UserTable.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)



class TenentRentAggrimentCreateView(APIView):

    def post(self, request):
        data = request.data
        unit_id = data['units']
        tenant_id = data['tenent_id']
        try:
            tenant_instance = UserTable.objects.get(user_id=tenant_id)
            unit_instance = Units.objects.get(unit_id=unit_id)
            data = {
                'units': unit_instance.unit_id,
                'tenent_id': tenant_instance.user_id,
                'rent_value': request.data.get('rent_value'),
                'start_date': request.data.get('start_date'),
                'end_date': request.data.get('end_date'),
            }
            serializer = TenentRentAggrimentSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Units.DoesNotExist:
            return Response({'error': 'Unit does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except UserTable.DoesNotExist:
            return Response({'error': 'Tenant does not exist'}, status=status.HTTP_404_NOT_FOUND)


class PropertyUnitsListView(APIView):
    def get(self, request):
        try:
            list_data=[]
            unit_ids = Units.objects.values_list('unit_id', flat=True)
            for i in unit_ids:
                unit = Units.objects.select_related('property_id').get(unit_id=i)
                userid = unit.property_id.property_owner_id.user_id
                owners=UserTable.objects.get(user_id=userid)
                ppr_id = unit.property_id
                owner_serializer=UserTableSerializer(owners)
                property_serializer = PropertySerializer(ppr_id)
                serializer = UnitSerializer(unit)
                list_data.append({"unit_data": serializer.data, "property_data": property_serializer.data,"owner_details":owner_serializer.data})
            return Response(list_data)
        except Units.DoesNotExist:
            return Response({"message": "Unit does not exist"}, status=404)


class PropertyUnitsCreateView(APIView):

    # def get(self,request,unit_id):
    #     try:
    #         unit = Units.objects.select_related('property_id').get(unit_id=unit_id)
    #         ppr_id=unit.property_id
    #         property_serializer=PropertySerializer(ppr_id)
    #         serializer = UnitSerializer(unit)
    #         return Response({"unit_data": serializer.data, "property_data": property_serializer.data})
    #     except Units.DoesNotExist:
    #         return Response({"message": "Unit does not exist"}, status=404)

    def post(self, request):
        data = request.data
        user_id = data["property_owner_id"]
        user_instance = UserTable.objects.get(user_id=user_id)
        property_data = {
            'property_id': data['property_id'],
            'features': data['features'],
            'propertyimage_link': data['propertyimage_link'],
            'addressline1': data['addressline1'],
            'pincode': data['pincode'],
            'created_at': date.today(),
            'city': data['city'],
            'state': data['state'],
            'country': data['country'],
            'property_owner_id':user_instance.user_id,
        }
        property_data['created_at']=date.today()
        unit_data = {
            'unit_size': data['unit_size'],
            'rent_value': data['rent_value'],
            'unit_bhk_size': data['unit_bhk_size'],
        }

        property_serializer = PropertySerializer(data=property_data)
        print(property_serializer)
        if property_serializer.is_valid():
            property_instance = property_serializer.save()
            print(property_instance)
            unit_data['created_at']=date.today()
            unit_data['property_id'] = property_instance.property_id
            unit_serializer = UnitSerializer(data=unit_data)

            if unit_serializer.is_valid():
                unit_instance = unit_serializer.save()
                return Response(
                    {"message": "Property and Unit created successfully."},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"errors": unit_serializer.errors},
                )

        return Response(
            {"errors": property_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
class Tenantunits(APIView):
    def get(self, request,tenant_id):
        time.sleep(11)
        # tenant_id = tenant_id
        try:
            user = UserTable.objects.get(user_id=tenant_id)
            tenant_rent_agreements = TenentRentAggriment.objects.filter(tenent_id=user)
            response_data = []
            for rent_agreement in tenant_rent_agreements:
                unit = rent_agreement.units
                property_details = unit.property_id

                data = {
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "email": user.email,
                    "addressline1": property_details.addressline1,
                    "rent_value": rent_agreement.rent_value,
                    "start_date": rent_agreement.start_date,
                    "end_date": rent_agreement.end_date,
                    "unit_rent_value": unit.rent_value
                }
                response_data.append(data)
            return Response(response_data)
        except UserTable.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)
        except TenentRentAggriment.DoesNotExist:
            return Response({"error": "No rent agreements found for the user"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)




class UserDetailsAPIView(APIView):

    def get(self, request,user_id):
        time.sleep(9)
        # user_id = request.query_params.get('user_id')
        try:
            user = UserTable.objects.get(user_id=user_id)
            user_data = {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "created_at": user.created_at,
            }
            return Response(user_data)

        except UserTable.DoesNotExist:
            raise Http404("User does not exist")

        except Exception as e:
            return Response({"error": str(e)}, status=500)
# class UserDetailsAPIView(APIView):
#     def get(self, request):
#         # user_id = request.query_params.get('user_id')
#
#         try:
#             user = UserTable.objects.get(user_id=user_id)
#             user_data = {
#                 "firstname": user.firstname,
#                 "lastname": user.lastname,
#                 "created_at": user.created_at,
#             }
#             return Response(user_data)
#
#         except UserTable.DoesNotExist:
#             raise Http404("User does not exist")
#
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)
