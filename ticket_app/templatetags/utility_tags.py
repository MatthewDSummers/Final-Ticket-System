from django import template

register = template.Library()


"""
These filters can be used in templates.

I. LENGTHIFY:

    It takes a list and the position of the item (`item_number`) . . . (not by index).
    I use Django's template forloop.counter (1,2,3) instead of actual index (0,1,2).
    So the function is coded as: `last_index = len(data_list)` to get the last item instead of the normal `last_index = len(data_list) -1

Example RETURNS:
    In cases of length of:
        1 item in list: Returns `item`
        2 items in list: Returns `item1 & item2`
        3 items in list: Returns `item1, item2, & item3`
        4 items in list: Returns `item1, item2, item3, & item4`

    Et cetera . . .

II. GET_ITEM:

    Pass a dict and one of its keys to get that key's value (useful inside forloops)

"""
@register.filter
def lengthify(item_number, data_list):
    if item_number == len(data_list): #This represents the last (or only) item of the list.
        return ''

    if len(data_list) > 2:
        if item_number == len(data_list) - 1: #this represents the 2nd to last item of the list
            return ', & '
        # elif item_number == len(data_list): ##redundant
        #     return ''
        else:
            return  ', '

    elif len(data_list) == 2:
        if item_number == 1:
            return ' & '
        # else:   ##redundant
        #     return ''
    else:
        return  ', '

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# lengthify Example usage:
"""
PYTHON:
    user_list = [
        {"full_name": "John"},
        {"full_name": "Jane"},
        {"full_name": "Jim"},
        {"full_name": "Bob"}
    ]

TEMPLATE:
    {% for person in user_list %}
        {{person.full_name}}{{forloop.counter|lengthify:user_list}}
    {% endfor %}

OUPUT:
    John, Jane, Jim, & Bob

"""


# get_item Example usage:
"""
PYTHON:
    product_dictionary = {
        1: {
            "id": 1,
            "name": "Smartphone",
            "brand": "Samsung",
            "price": 999.99
        },
        2: {
            "id": 2,
            "name": "Laptop",
            "brand": "Apple",
            "price": 1499.99
        }
    }

    store_list = [
        {
            "id": 1,
            "name": "ElectroVolt",
            "products": [1, 2]
        },
        {
            "id": 2,
            "name": "GadgetMania",
            "products": [2]
        }
    ]

TEMPLATE:
    {% for store in store_list %}
        {% with products=store.products %}
            <h3>{{ store.name }}</h3>
            <ul>
            {% for product_id in products %}
                {% with product=product_dictionary|get_item:product_id %}
                    <li>{{ product.name }} - Brand: {{ product.brand }} - Price: ${{ product.price }}</li>
                {% endwith %}
            {% endfor %}
            </ul>
        {% endwith %}
    {% endfor %}

OUTPUT: 
    ElectroVolt
    - Smartphone - Brand: Samsung - Price: $999.99
    - Laptop - Brand: Apple - Price: $1499.99

    GadgetMania
    - Laptop - Brand: Apple - Price: $1499.99
"""

# TODO: lengthify is a useful function, but probably not the best name; unregister and rename it later 
