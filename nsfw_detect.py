from nudenet import NudeDetector
import cv2


class NSFWDetector:

    def __init__(self, image):
        self.labels = [
            "FEMALE_GENITALIA_COVERED",
            "BUTTOCKS_EXPOSED",
            "FEMALE_BREAST_EXPOSED",
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_BREAST_EXPOSED",
            "ANUS_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
            "ANUS_COVERED",
            "FEMALE_BREAST_COVERED",
            "BUTTOCKS_COVERED",
        ]
        self.nude_detector = NudeDetector()
        self.image = image
        self.threshold = 0.2

    def get_is_nsfw(self):
        is_nsfw = False
        detected_labels = self.nude_detector.detect(self.image)
        for label in detected_labels:
            if label['class'] in self.labels and label['score'] > self.threshold:
                is_nsfw = True

        if is_nsfw:
            print("görsel nsfw içeriyor")
            return True

        print("görsel nsfw içermiyor")
        return False

    def get_censored_image(self, blur_only_detected_parts=False):
        if blur_only_detected_parts:
            return self.nude_detector.censor(self.image, self.labels)
        img = cv2.imread(self.image)
        new_path = f"images/{self.image.split('/')[-1].split('.')[0]}-whole-censored.jpeg"
        cv2.imwrite(
            new_path, cv2.GaussianBlur(img, (45, 45), 0))
        return new_path
