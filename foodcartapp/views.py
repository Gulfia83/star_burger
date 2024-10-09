from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.templatetags.static import static
from phonenumbers import parse, is_valid_number
from phonenumbers.phonenumberutil import NumberParseException

from .models import Order, OrderItem, Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return Response(dumped_products)


@api_view(['POST'])
def register_order(request):
    data = request.data
    products = data.get('products')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    phonenumber = data.get('phonenumber')
    address = data.get('address')
    if not products or not isinstance(products, list):
        return Response(
            {"error": "Products key not presented or not list"},
            status=status.HTTP_400_BAD_REQUEST
            )
    for product in products:
        try:
            Product.objects.get(id=product['product'])
        except Product.DoesNotExist:
            return Response(
                {"error": "Product ID doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
                )
    if not firstname or not isinstance(firstname, str):
        return Response(
            {"error": "The key 'firstname' is not specified or not str."},
            status=status.HTTP_400_BAD_REQUEST
            )
    if not lastname or not isinstance(lastname, str):
        return Response(
            {"error": "The key 'lastname' is not specified or not str."},
            status=status.HTTP_400_BAD_REQUEST
            )
    if not phonenumber or not isinstance(phonenumber, str):
        return Response(
            {"error": "The key 'phonenumber' is not specified or not str."},
            status=status.HTTP_400_BAD_REQUEST
            )
    try:
        parsed_number = parse(phonenumber)
    except NumberParseException:
        return Response(
            {"error": "The phonenumber is not valid"},
            status=status.HTTP_406_NOT_ACCEPTABLE
            )
    if not is_valid_number(parsed_number):
        return Response(
            {"error": "The phonenumber is not valid"},
            status=status.HTTP_406_NOT_ACCEPTABLE
            )
    if not address or not isinstance(address, str):
        return Response(
            {"error": "The key 'address' is not specified or not str."},
            status=status.HTTP_400_BAD_REQUEST
            )
    else:
        order = Order.objects.create(
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber,
            address=address
            )
        order_items = [
            OrderItem.objects.create(
                product=Product.objects.get(id=product['product']),
                order=order,
                quantity=product['quantity']
            ) for product in products
        ]

    order = Order.objects.create(
        firstname=data['firstname'],
        lastname=data['lastname'],
        phonenumber=data['phonenumber'],
        address=data['address']
        )
    order_items = [
        OrderItem.objects.create(
            product=Product.objects.get(id=product['product']),
            order=order,
            quantity=product['quantity']
        ) for product in data['products']
    ]

    return Response(data)
