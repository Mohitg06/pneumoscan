# The following method accepts path of an image, performs inference on
# construction machines detector, PPE, hard-hat detector models and generates a status summary.
def generate_status_summary(image_path):
    image_byte_array = []

    num_cap = 0
    num_ppe = 0
    num_face_mask = 0
    num_gown=0

    # Open the image.
    with open(image_path, "rb") as image:
        image_byte_array = bytearray(image.read())

    # Count number of gowns and caps
    machine_detection_result = json.loads(predictor_machine_detection.predict(image_byte_array).decode('utf-8'))
    for output in machine_detection_result['outputs']['detections']:
        if output[5] > 0.65:
            if output[4] == 'CAP':
                num_cap += 1
            if output[4] == 'GOWN':
                num_gown += 1

    # Count number of personal protective equipments(PPEs)
    ppe_detection_result = json.loads(predictor_ppe_detection.predict(image_byte_array).decode('utf-8'))
    for output in ppe_detection_result['output']:
        if output['score'] > 0.5:
            num_ppe += 1

    # Count number of face masks
    face_mask_detection_result = json.loads(predictor_hard_hat_detection.predict(image_byte_array).decode('utf-8'))
    for i in range(len(face_mask_detection_result['boxes'])):
        if face_mask_detection_result['scores'][i] > 0.5:
            num_face_mask += 1

    # Create and return the summary.
    if num_ppe == num_face_mask == 0:
        current_status = "Alarm : " + str(num_gown) + " gown(s), " + str(
            num_cap) + " cap(s), no medical staff found."
    elif (num_ppe == num_face_mask):
        current_status = "No Alarm : " + str(num_gown) + " gown(s), " + str(num_cap) + " cap(s), " + str(num_face_mask)
        "face mask(s)" + str( num_ppe) + " medical staff found."
    elif num_ppe > num_face_mask:
        current_status = "ALARM    : " + str(num_ppe) + " Medical Workers(s) wearing PPE but " + str(
            num_face_mask) + " wearing face masks, " + str(num_gown) + " gown(s), " + str(
            num_cap) + " cap(s) found."
    elif num_face_mask > num_ppe:
        current_status = "ALARM    : " + str(num_face_mask) + " Medical Worker(s) wearing face masks but " + str(
            num_ppe) + " workers wearing PPE, " + str(num_gown) + "gown(s), and " + str(
            num_cap) + " cap(s) found."
    return current_status