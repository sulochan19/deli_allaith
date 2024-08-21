from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from .models import Order, Food, Cart, OrderContent
from django.contrib import messages


@login_required
@staff_member_required
def dashboard_admin(request):
    orders = Order.objects.count()
    customers = User.objects.count()
    completed_orders = Order.objects.filter(delivery_status="Completed",   order_timestamp__date=timezone.now().date())
    top_customers = User.objects.filter().order_by('-total_sale')
    latest_orders = Order.objects.filter().order_by('-order_timestamp')
    sales = 0
    for order in completed_orders:
        sales += order.total_amount

    context = {
        'orders':orders,
        'customers':customers,
        'sales':sales,
        'top_customers': top_customers,
        'latest_orders':latest_orders,
    }
    return render(request, 'admin_temp/index.html', context)

@login_required
@staff_member_required
def orders_admin(request):
    orders = Order.objects.filter().order_by('-order_timestamp')
    items = Cart.objects.filter(user=request.user.id).count()
    orders_with_contents = []
    for order in orders:
        order_contents = OrderContent.objects.filter(order=order)
        orders_with_contents.append({
            'order': order,
            'contents': order_contents
        })
    return render(request, 'dashboard.html', {'orders_with_contents': orders_with_contents,'item_count':items})

def index(request):
    food = Food.objects.filter(status = 'Enabled',quantity_available__gt=0)
    items = Cart.objects.filter(user=request.user.id).count()
    return render(request, 'index.html', {'food':food,'item_count':items})

@login_required
@staff_member_required
def confirm_delivery(request, orderID):
    order = Order.objects.get(id=orderID)
    order.confirmDelivery()
    order.save()
    return redirect('deli_allaith:orders_admin')

@login_required
@staff_member_required
def add_food(request):
    if request.method == "POST":
        name = request.POST['name']
        status = request.POST['status']
        content = request.POST['content']
        sale_price = request.POST['sale_price']
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)

        if (name == "") or (status is None) or (content == ""):
            foods = Food.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'admin_temp/foods.html', {'foods': foods, 'error_msg': error_msg})

        food = Food.objects.create(name=name, status=status, content_description=content, sale_price=sale_price, image=filename)
        food.save()
        foods = Food.objects.filter()
        success_msg = "Please enter valid details"
        return render(request, 'admin_temp/foods.html', {'foods': foods, 'success_msg': success_msg})
    return redirect('hotel:foods_admin')

def food_details(request, foodID):
    food = Food.objects.get(id=foodID)
    return render(request, 'user/single.html', {'food':food})

@login_required
def addTocart(request, foodID):
    food = Food.objects.get(id=foodID)
    user = User.objects.get(id=request.user.id)
    cart = Cart.objects.create(food=food, user=user)
    cart.save()
    return redirect('deli_allaith:index')

@login_required
def delete_item(request, ID):
    item = get_object_or_404(Cart, id=ID, user=request.user)
    item.delete()
    return redirect('deli_allaith:cart')

@login_required
def cart(request):
    user = User.objects.get(id=request.user.id)
    items = Cart.objects.filter(user=user)
    item_count = Cart.objects.filter(user=request.user.id).count()
    total = 0
    for item in items:
        total += item.food.sale_price
        
    return render(request, 'cart.html', {'items': items, 'total':total,'item_count': item_count})

@login_required
def placeOrder(request):
    customer = User.objects.get(id=request.user.id)
    items = Cart.objects.filter(user=request.user)
    if items:
        for item in items:
            food = item.food
            if food.quantity_available > 0:
                order = Order.objects.create(customer=customer, order_timestamp=timezone.now(), 
                delivery_status="Pending", total_amount=food.sale_price)
                order.save()
                orderContent = OrderContent(food=food, order=order)
                orderContent.save()
                item.food.quantity_available -= 1
                item.food.save()
                item.delete()
        messages.success(request,"Order Placed Successfully!")
    return redirect('deli_allaith:index')

@login_required
def my_orders(request):
    get_object_or_404(User,id=request.user.id)
    user = get_object_or_404(User,id=request.user.id)
    items = Cart.objects.filter(user=request.user.id).count()
    orders = Order.objects.filter(customer=user).order_by('-order_timestamp')

    orders_with_contents = []
    for order in orders:
        order_contents = OrderContent.objects.filter(order=order)
        orders_with_contents.append({
            'order': order,
            'contents': order_contents
        })

    return render(request, 'orders.html', {'orders_with_contents': orders_with_contents,'item_count':items})


        
