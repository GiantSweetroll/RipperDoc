import file_operations
import tensorflow as tf
import requests
import numpy as np
import constants
import base64
import io
from PIL import Image
# import docker

def save_base64():
    image = file_operations.load_image('L:/For Machine Learning/Logo Recognition/selenium/__unused/Apple logo/Apple logo (39).png')
    image = file_operations.convert_png_to_jpg(image)

    base64str:str = file_operations.get_as_base64_from(image).decode('utf-8')

    f = open('test_image.txt', 'w')
    f.write(base64str)
    f.close()

    return base64str

def check_image_input(image_bytes:str):
    imgdata = base64.b64decode(image_bytes)
    with open('test_image.jpeg', 'wb') as f:
        f.write(imgdata)

def from_curl(image_bytes:str):
    # Decode image into tensor
    base64_bytes = image_bytes.encode('ascii')
    im_file = io.BytesIO(base64.b64decode(base64_bytes))
    image = Image.open(im_file)

    # Format input
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    input_arr = tf.image.resize(input_arr, [constants.image_width, constants.image_height])  # Resize image to fit neural network input
    input_arr = np.array(input_arr)     # Convert it back to numpy array
    input_arr /= 255        # Apply normalization

    # Make request to serving docker container
    url = 'http://localhost:8501/v1/models/ripperdoc:predict'
    payload = {"instances" : input_arr.tolist()}
    response = requests.post(url = url, json = payload)
    
    # Process prediction
    r_json = response.json()        # JSON data of response
    pred_np = np.array(r_json['predictions'])       # Get prediction list and convert it to numpy array
    pred:str = constants.labels[int(pred_np.argmax().__str__())]        # Apply argmax and convert it to label
    print(pred)

# temp = save_base64()
# print(temp)
# temp = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAC0APADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3q2YtbqScnn+dS1Da/wDHsn4/zqagBkv+rNVqsy/6s1WoAKKKKACiiigAooooAKKKKACiiigAoopKAFoopKAFooNJQAtFFFABRRRQAUlFFABRRRQAUUUUAT2v/Hsn4/zqaobX/j2T8f51NQAyX/Vmq1WZf9WarUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABSUtFACUUtFACUUtFAE1r/x7J+P86mqG0/49k/H+dTUAMl/1ZqtVmX/Vmq1ABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBNa/wDHsn4/zqaobX/j2T8f51NQAyX/AFZqtVmX/VmqcsixRM7ttVRkn0oAeTRXEX/iS8u7nyrNjFGW2rtHzNXZwqywoHOWCjJ9ayp1lUbSM6dRTvYkooorU0CiiigAozRXKeIfEptGkgtpAuz78nv7VdOm5ysjDEYmnh4c8zqgfWlrH8MpdLocL3jM00pMh3nkAnIH5VsVMlZ2NIS5oqVtwooopFhRRRQAhOKNw/8A1V5N8W/ihP4WkXRtHKjUnQPJKwz5SnoAPU1L8DzrF9oWoa1q91cXDXkwETTMTwuQSPbJ/SgD1WiiigAooooAKTPNLWJr+sjS4Fji5uJc7QBkgeuKaVwNoMDS1yvhuW8uL+Se6YkFMAEk9+9dVQ1YE7hRRRSAmtf+PZPx/nU1Q2v/AB7J+P8AOpqAKmp3kdhp0tzKCUTGQOvJA/rXN32sWuq6XLBa3CxyvgYkO3jvW34iiE+hXMZOAdvI/wB4VwZ0pMf61v0rysdj44ep7OXVf5idCvV/hq6LenrpmkTrPdXAuJ15VIhkKfr61vW3ijT7iQIzNET0Ljj865b+y4/+ejfkKdFoomlWNJGLMcdq4qWaQTUYErB4qmtIpI9BVgygggg88UtVNNsxp9mlsJHk2/xOc/5FW6+gi21dla21CqFzqsNuduC5+oA/M1neLNa/sjTlEYzPM2yNfU/4VwweWY755Gkc9STXZQwzqavY8zH5ksM1FK7PQU8R2LNslLQHs0g+U/iOK5aHSdKs7r7dqd++oSK5dY41yinrn3rKVzH90kUkkzSD52JrrWD5XeLPIqZt7SznBNrY6pfH+lRy7J47mCMHHmsmVH5V1Ftcw3cCzwSpJE4yrKcgivGL4tJJHa28QlmmYIq+56V6d4U8Pjw7pK2jTvK7He+T8oJ7KOwrkxFGNJ2R6+W4ypiU3JG9SHgdM0tYPjLxFH4V8JahrDjc0Ef7tP7zk4UfmRXKeoQeJPHnh/woQuq36JMRkQp8zkfQVg6f8afBuoXKwfbZICTw88RVfz7V8t6nqV3q1/NfX0zTXEzlndj1Jqpk0Ae8eMND8ETeKrjxD4h8UrPBOwaOzs/mYqOxIzxW9p/xy8G2aQ2FtZXdvZxKEQrGNqqPbOa+ack9TSqCxwOaAPuHSNb07XrBL3TbqO4t2/iQ9PYjsa0K81+EPgRvCuhC/u5pft1+gaSEuQka9QMf3vf3r0qgArO1PWrPSgouJCZX/wBXDGNzt9AKsX95Hp9hcXkp+SFC5+gFcloiPNC2qXuHvLr52Y/wqeij0AFVFXFc0j4tMfzSaNqIi/vhAx/IHNZl3rOk6jei7truF3ZAoVlO9Mdtvrz3Fab3QHpVN7iNXLiJAx6kAZq7aktiQeIU0xCItJvp8n5pcAZ/Amt3SNestZRjbsySp9+GVdrr9RXMTXW4+grT0LTj9v8Atu3lV257f/XpOKtcE3ex1FFFRTOyrhThmO0HHT3/AK1mWW7X/j2T8f51NUNr/wAeyfj/ADqagDJ8Su0fh+6ZTgjZz/wMV599rm/56Gu28cHHg6/Ocf6v/wBGLXjvm/7R/OvGzHASxFVTXbt5s+hymEJUXzNb/ojrPtc3/PQ1reHbkvqyLK+cqcD3rz3zf9o/nUtteyWlzHPDIVkRsqc1y0MrnTqKbW3kd1bD0503GLV2e5UVheHPEcOvQMEjZJogPMU9OfQ/ga3e1fRpnyc6bpy5Jbnm/jyV28U6fbt/qhCzr9elZhlA471vfEi0ZVsNUjHMLGNz7N/9euPtZdwBznNevg5LksfGZxCSruRfLk0hNNDZFIWruueLzXRPoSxr4r095OgkOM+u04/WvW8V4hc3DQsssbbGjIZT6GvS/CfiqDxFasvK3UIHmrjj6ivIxsHzcyPqsjrWg4Pc6SvJv2gpZU8BWqJkK98gfHptY/zr1muJ+LGgvr/w71KCFd1xbgXMQxnJTkj8V3Vwn0B8hZJopSMZpKACrukFBrNiZMeX9oj3Z6Y3DNUqVTg5oA+7oNvkR7Mbdoxj0xUleQ/Cj4pw65b2nh3UUlGqIuyOULlZlUdSR0IA5zXro6UAc/443HwhfhM5KAH6ZFYMN2q2kShsYUYx9K7LVrQX2lXNs3SSMrXnenW75Mcn30O3n2rWnqjObszQa63dM1E0zN2xVwWJo+xuO1XYi5kztIql+eK9F0zYdPhaMghlzxXIvp5ZMGrGkarLplzb6fMrSQTPtjIPKHr+VTOLa0Ki0nqdjUE/Dxjtk1P6VBdcRq46I2T9OhrE1Ltp/wAeyfj/ADqaobX/AI9k/H+dTUAc746G7wbfj/rn/wCjFrxnyj/eFe767pw1bRrixaQxiXb8wGcYYH+lYFl4J0m1T97Gbl/70h/oK78NXo06bU97nJVq4+NTlwzSjbr3/qx5P5R/vCnxWss8qxRDe7naqjua9SvvBGlXYJhV7Zv9g5H5GrGieFLLR5POBaafs7j7v0FbvFUOW8U7mccTm3tLScbd7E3hrRl0TSI4CQZn+eVgOrH/AA6Vs5oFFeVKTbuz0G29WUtV0+LVdNnsph8kqYz6Hsa8QnS40bUptPu1KyRNjPYjsfxr3yue8S+EbHxKimYmG5jGEnQcgeh9RW1CryaM8/G4NV46bnmKXikD5qSS8X+9Xaad8MLK2k3Xd9NcgfwKNg/TmtO48B6U8eLTzrV/7yuWH4g12fXY3seI8kqWueT3BkuVYg7IxyzGvUvAGgtpGjG4mQpcXZDsrdVXsD796TTfAdva3qXF5cG68ttyR7AqZHQkd/Wuwrlr1lPSJ6+AwUqK5phTXUOhUgEEYINLQeRXMemfJfxW8FP4S8TyvDH/AMS68Yy27AcLnqv4fyrga+2vEfhrTfFWlPp+qQ+ZCeQRwyN6g15/ZfAHwzbXvnXFzeXUQORCxCj8SOTQB8y0q19dah8JPBl/Y/ZRpEducfLLAxVx+Pf8a5zTvgFoFlqa3U99c3cKMGFu6qAcdiR1oAq/AzwO2l6a3iW/i23N2my2VhykXdv+BfyHvXsvvTI0WONUQBUUAKAMACnUABGfp3rktSsRY6l5+MRyHmutqC7tI7yFopFBBHWqjKzE1dGdbW6SRhuOlK0ESttyKqJoM8RKRTMI/Te38s1N/wAI5Gy/NKd1ac6M+RkrwIEzkCs6xtlvdXSdRmKEfK3Y+9SHw7MXw0pZPRnYj8s4rdtbVLWLYvJ7n1pSqaWQ1DW5Pz+FIVDKVOMHrmlorI0J7T/j2T8f51NUNp/x7J+P86moAjmIETZOOlVgysMggj2p2ptClhI1wcRKVJP/AAIY/WsqzmswogiuMthmYKCAc5J//VQBpbl9RSgg9DmuaMFtJkLqQUgdBnI6/r6VqaOqfZ5HjmaRGfIJUj+dAGlRRRQAUVDcXEdtH5kpIXOMgZqE6rY4P+kp8vBoAt7lzjIzQGB6EVh3iWs9yz/blTcRwCfToKbai3tJkuZL4MnzDoQOpzj2GaAN+kqp/athjP2lMeuasxypLGHRgynoRQA6iimSyrBC8rnCopY8Z4FADiQOpFG4ZxkZrGvJbO/YNHeLGcFe/r1qskVsl3HL/aGVDZAIOOCP17UAdESBjJ60BgehFY91cW1z5ca38YG7O45BGemD9agZLdZGR76ONs8rgjGOMD2OOaAOgBBGRzRVCyu7WKNIPtKM5Y4Az1J6Cr5oAKCQBk8Ciq19A1xbmNGVTkEluw70AWNy+ooyPWsFFtmIK3ybc55B9ev1q0bq1hs1j+2IAYgFLfdI/vUAam5cfeH50BgehBrARIFOPtsZK8kEHB6HB9uOK1LC1WCPcHD71X5h3AFAFyiiigCe0/49k/H+dTVDaf8AHsn4/wA6moAjuFV4GVlDA44Iz3qgLK2ByIIskYJ2CtCX/Vmq1AFf7Fa4wLaIc/3BUyIsYwqhR6AU6igAooooAa8aOMOqsPRhmoTZWpBAtogCcn5Bz/nA/KrFFAFcWFoP+XaEY5B2CnG0gKhDDHsH8JUYqaigCv8AYrXdn7NDn12DNTIoQbQAF9h0p1JQAUjKGUqwBBGCDS0UAQm1g3M3kR7m6naOaatnbqMC3hAzkYQcVYooAgFnbAAeRFgHIGwcUptYGkLtBGWPUlQT/nipqKAIhbQKQywxgj0UCpaKKACkIBzmlooArNp9oz7jbRE/7gpxtLdkCtbxEAYA2DAHpU9FAEAs7bfv8iIN67BUwUKAqjCjge1LRQAUUUUAT2n/AB7J+P8AOpqwvB2vweJ/CljrNtDJDFch8RyY3LtdlOce6mt2gBkv+rNVqsy/6s1WoAKKKKACiiigAooooAKKKKACkpaSgAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAOO+Cv/JI9D/7eP8A0fJXfVwHwU/5JHof/bx/6Pkrv6BvcZL/AKs1WqzL/qzVagQUUUUAFFFFABRRRQAUUUUAFJS0lABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAC0lFFABRRRQBT8K+HbTwp4btNEsJJ5La237GnYFzudnOSAB1Y9q2aKKBvcZL/qzVaiigQUUUUAFFFFABRRRQAUUUUAJRRRQAUUUUAFFFFABRRRQAUUUUAFLRRQAlFFFABRRRQAUUUUAf/Z"
# from_curl(temp)
# check_image_input(temp)

# docker_client = docker.DockerClient()
# serving_container = docker_client.containers.get("ripperdoc-backend_serving_1")
# ip = serving_container.attrs['NetworkSettings']['Networks']['ripperdoc-backend_default']['IPAddress']
# print(ip)