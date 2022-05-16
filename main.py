import base64
import numpy as np
import cv2
from google.cloud import storage
import psycopg2
import os
import ast
import urllib.parse as urlencode


def qr_analyzer(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    Returns:
        If successful, a dictionary with the plot ID stored within the QR
            code and a url connected to the image blob.
        If unsuccessful, None.
    """

    event = ast.literal_eval(base64.b64decode(event["data"]).decode("UTF-8"))

    if "data" in event:
        event["data"] = event["data"].decode("UTF-8")
        output = {"QR": None, "URL": None}
        print(f"Did I get the base64 through: {event['data'][0:9]}")
        pubsub_message = base64.b64decode(event["data"])
        test_arr = np.frombuffer(pubsub_message, dtype=np.uint8)
        new_img = cv2.imdecode(test_arr, flags=cv2.IMREAD_COLOR)

        results = cv2.QRCodeDetector().detectAndDecode(new_img)
        if results[1] is None:
            print("No data could be retrieved from the image.")
        else:
            print("ID in QR Code: ", results[0])
            output["QR"] = results[0]
            if checkid(output["QR"]) is True:
                url = storage_add_fetch(pubsub_message, event, context)
                output["URL"] = url
                insertimage(output["QR"], output["URL"])
                print(
                    "Output data from QR: "
                    + output["QR"]
                    + "\nOutput url: "
                    + output["URL"]
                )
                return output

    print("Data was not found...")
    return None




def getconnection():
    """Attempts to get a connection to our database.
    Arguments:
        Void
    Returns:
        The connection to the database if successful
    """
    unix_socket = "/cloudsql/{}".format("unfold-usf:us-central1:postgres-instance-usf")
    dbpass = os.environ.get("dbpassword")

    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password=dbpass,
        host=unix_socket,
    )
    print(conn)
    return conn


def checkid(plotid):
    """Checks to see if the plotid is in the plots table.
    Arguments:
        plotid: an integer
    Returns:
        True, if the id is the table.
        False, if the id isn't in the table.
    """
    conn = None
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute("PREPARE select_statement as SELECT * FROM plots where id = $1")
        cursor.execute("EXECUTE select_statement (%s)", (plotid,))

        if cursor.fetchone() is not None:
            print("in cursor fetchone print")
            return True
        else:
            return False

    except (Exception, psycopg2.Error) as error:
        print("Error occurred while checking id", error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Connection to database closed")


def insertimage(plotid, url):
    """Attempts to insert an image URL into the images table.
    Arguments:
        plotid: an integer
        url: a string
    Returns:
        Void
    """
    print("Adding to plot id:", plotid, "the image:", url)

    conn = None
    try:
        conn = getconnection()
        cursor = conn.cursor()

        count_query = "SELECT COUNT(*) FROM images"
        cursor.execute(count_query)
        countrow = cursor.fetchone()
        count = countrow[0]
        imageid = count + 1

        cursor.execute(
            """INSERT INTO images(id, plot_id, image_handle)
               VALUES (%(id)s, %(plot_id)s, %(image_handle)s);""",
            {
                "id": imageid,
                "plot_id": plotid,
                "image_handle": url,
            },
        )

        conn.commit()
        print("Record inserted into images table")

    except (Exception, psycopg2.Error) as error:
        if conn:
            conn.rollback()
        print("Failed to insert record into images table", error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Connection to database closed")


def storage_add_fetch(data, event, context):
    """Triggered from a message on a Cloud Pub/Sub topic 'Camera_rig'. Adds image from encoded dictionary in event
        dictionary data to Google Cloud Storage and returns a URL that references that image.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    # This creates a client object that then creates a bucket
    # object. This grants us the ability to edit the accessed
    # bucket
    client = storage.Client()
    bucket = client.bucket(event["bucket"])

    # This creates a blob object which then gets the date
    # from the upload function
    blob = bucket.blob(event["filename"])

    blob.upload_from_string(data, content_type="image/jpeg")

    # Finally, a url is generated for the bucket. The expire_tuple
    # is a tuple representing the time the url life expires
    urlFilename = urlencode.quote_plus(event["filename"])
    url = "/".join(
        ["https://storage.cloud.google.com", event["bucket"], urlFilename]
    )
    return url
