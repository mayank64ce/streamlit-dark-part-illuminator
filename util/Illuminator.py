import cv2
import numpy as np

import os

class Illuminator:
    from .config import alpha, gamma, r, eps

    def adjust_gamma(self, image, gamma=1.0):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")
        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def illuminate(self, img_path):

        # global alpha, gamma, r, eps

        I_rgb = cv2.imread(img_path)

        I_r = I_rgb[:,:,0].astype('double')
        I_g = I_rgb[:,:,1].astype('double')
        I_b = I_rgb[:,:,2].astype('double')

        I = (I_r + I_g + I_b) / 3.0
        I = I.astype('uint8') # to comment or not to comment

        I_gamma = self.adjust_gamma(image=I, gamma=self.gamma) # WTF?

        I_he = cv2.equalizeHist(I_gamma)

        O = (1-self.alpha)*I_gamma + (self.alpha) * I_he

        _, W = cv2.threshold(I, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,)

        W_tilde = cv2.ximgproc.guidedFilter(I, W, radius = self.r, eps=self.eps).astype('double') / 255.0

        O_tilde = (1-W_tilde) * O + (W_tilde)*I

        O_rgb = np.zeros(I_rgb.shape)

        O_rgb[:,:,0] = I_r * (O_tilde/I)
        O_rgb[:,:,1] = I_g * (O_tilde/I)
        O_rgb[:,:,2] = I_b * (O_tilde/I)

        # print(O_rgb)

        # O_rgb = O_rgb.astype('uint8')

        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/out.png')

        status = cv2.imwrite(out_path, O_rgb)

        # print("hello fucker!", status, out_path)

        out = cv2.imread(out_path)

        out = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)

        return out