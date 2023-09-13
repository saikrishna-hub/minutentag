"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""
import boto3


def get_s3_objects(bucket, prefix=''):
    s3 = boto3.client('s3')

    kwargs = {'Bucket': bucket}
    next_token = None
    if prefix:
        kwargs['Prefix'] = prefix

    while True:
        if next_token:
            kwargs['ContinuationToken'] = next_token
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get('Contents', [])

        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix):
                yield obj
        next_token = resp.get('NextContinuationToken', None)

        if not next_token:
            break

for s3_object in get_s3_objects('your_bucket_name', 'your_prefix'):
    # Process each S3 object as needed
    print(s3_object)


"""
Please, full explain this function: document iterations, conditionals, and the
function as a whole
"""
def fn(main_plan, obj, extensions=[]):
    """
    ->To process a list of items and examine quantity and status based on various conditions involving a main plan,
         object properties, and a list of extensions.
    ->Initialize items list, and boolean flags for later use.
    ->A loop iterates through each extension in the extensions list.
    ->It populates the ext_p dictionary with extension prices as keys and their quantities as values.
    ->The function then iterates through each item in the 'items' data of the obj parameter.
    ->It processes each item and creates dictionary product for each item with an 'id' key representing the item's ID.
    ->After reaching item processing loop, there are several conditionals to be checked.
    ->first: if item.price.id != main_plan.id and item.price.id not in ext_p:
    ->checks if the item's price ID is not equal to the main plan's ID and is not found in the ext_p dictionary.
    ->If both conditions are met, it marks the product as 'deleted,' and the cd flag is set to True.
    ->second: elif item.price.id in ext_p: checks if the item's price ID is found in the ext_p dictionary.
    ->If it is, it retrieves the quantity associated with that price from ext_p.
    ->If the quantity is less than 1, it marks the product as 'deleted.'
    ->Otherwise, it sets 'qty' key in the product dictionary to retrieved quantity and removes the price from ext_p.
    ->Third: elif item.price.id == main_plan.id: checks if the item's price ID is equal to the main plan's ID.
    ->If it is, it sets the sp (Special Plan) flag to True.
    ->After processing each item, the product dictionary is appended to the items list.
    ->After processing all items, a conditional check if not sp: checks if there was no item with a price ID
    ->matching the main plan's ID. If condition is met, it adds product for main plan with quantity of 1 to items list.
    ->Finally, there's another loop that iterates through the remaining extension prices in the ext_p dictionary.
    ->For each price with a quantity greater than or equal to 1, product dictionary is created and added to items list.
    ->The function returns the items list, which contains dictionaries representing the processed items,
    ->including their IDs, quantities, and status flags.

    In summary, this function processes a list of items, calculates quantities,
    and marks certain items as 'deleted' based on conditions related to a main plan, object properties,
    and a list of extensions. The function returns a list of processed items
    """
    items = []
    sp = False
    cd = False

    ext_p = {}

    for ext in extensions:
        ext_p[ext['price'].id] = ext['qty']

    for item in obj['items'].data:
        product = {
            'id': item.id
        }

        if item.price.id != main_plan.id and item.price.id not in ext_p:
            product['deleted'] = True
            cd = True
        elif item.price.id in ext_p:
            qty = ext_p[item.price.id]
            if qty < 1:
                product['deleted'] = True
            else:
                product['qty'] = qty
            del ext_p[item.price.id]
        elif item.price.id == main_plan.id:
            sp = True


        items.append(product)

    if not sp:
        items.append({
            'id': main_plan.id,
            'qty': 1
        })

    for price, qty in ext_p.items():
        if qty < 1:
            continue
        items.append({
            'id': price,
            'qty': qty
        })

    return items


"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""
class Caller:
    add = lambda a, b : a + b
    concat = lambda a, b : f'{a},{b}'
    divide = lambda a, b : a / b
    multiply = lambda a, b : a * b

"""
Function fn refactored to one line to call Caller class with any method or else return None
"""
def fn(fn_to_call, *args):
    return getattr(Caller, fn_to_call)(*args) if hasattr(Caller, fn_to_call) else None



"""
A video transcoder was implemented with different presets to process different videos in the application. The videos should be
encoded with a given configuration done by this function. Can you explain what this function is detecting from the params
and returning based in its conditionals?
"""

"""
This function, fn, is designed to select a list of video encoding presets from a given configuration (config)
based on two input parameters: w(width) and h(height). 
The function calculates the aspect ratio(ar) of the video based on the provided width and height and then determines
which list of presets to select based on the aspect ratio and the configuration.
Here's a step-by-step explanation of what the function is doing:
Calculate the aspect ratio (ar) of the video by dividing width by height.
The function uses conditional statements to select a list of presets (v) based on the calculated ar and the config.
If ar is less than 1 (indicating a portrait or tall video), it selects a list of presets from config['p'] 
where the width of the presets (r['width']) is less than or equal to the provided w.
If ar is greater than 4/3 (indicating a landscape or wide video with a wider aspect ratio), 
it selects a list of presets from config['l'] 
where the width of the presets (r['width']) is less than or equal to the provided w.
If neither of the above conditions is met (meaning the aspect ratio is between 1 and 4/3), 
it selects a list of presets from config['s'] 
where the width of the presets (r['width']) is less than or equal to the provided width.
The function returns the selected list of presets (v) based on the conditions.
In summary, this function helps choose the appropriate video encoding presets from the given configuration 
based on the aspect ratio and the provided width of the video. 
The selected presets are then returned as a list. 
The function's purpose is to tailor the encoding settings to match the characteristics of the input video.
"""
def fn(config, w, h):
    v = None
    ar = w / h

    if ar < 1:
        v = [r for r in config['p'] if r['width'] <= w]
    elif ar > 4 / 3:
        v = [r for r in config['l'] if r['width'] <= w]
    else:
        v = [r for r in config['s'] if r['width'] <= w]

    return v


"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""
import requests

class Helper:
    DOMAIN = 'http://example.com'
    SEARCH_IMAGES_ENDPOINT = 'search/images'
    GET_IMAGE_ENDPOINT = 'image'
    DOWNLOAD_IMAGE_ENDPOINT = 'downloads/images'

    AUTHORIZATION_TOKEN = {
        'access_token': None,
        'token_type': None,
        'expires_in': 0,
        'refresh_token': None
    }

    def _api_request(self, endpoint, method='GET', params=None, data=None):
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']

        headers = {
            'Authorization': f'{token_type} {access_token}',
        }

        URL = f'{self.DOMAIN}/{endpoint}'

        send = {
            'headers': headers,
            'params': params,
            'data': data
        }

        if method == 'GET':
            response = requests.get(URL, **send)
        elif method == 'POST':
            response = requests.post(URL, **send)
        else:
            raise ValueError('Invalid HTTP method')

        return response

    def search_images(self, **kwargs):
        return self._api_request(self.SEARCH_IMAGES_ENDPOINT, params=kwargs)

    def get_image(self, image_id, **kwargs):
        endpoint = f'{self.GET_IMAGE_ENDPOINT}/{image_id}'
        return self._api_request(endpoint, params=kwargs)

    def download_image(self, image_id, **kwargs):
        endpoint = f'{self.DOWNLOAD_IMAGE_ENDPOINT}/{image_id}'
        return self._api_request(endpoint, method='POST', data=kwargs)
