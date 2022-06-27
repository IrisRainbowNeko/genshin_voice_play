import string
import PIL.Image as Image
import matplotlib.pyplot as plt
import cv2
import numpy as np
import yaml
import torch
from models.model_bbox import XVLM
from models.tokenization_bert import BertTokenizer
from torchvision import transforms

class XVLMInterface:
    def __init__(self, config_path = './configs/Grounding_bbox_genshin.yaml', checkpoint = './output/genshin_v1/checkpoint_best.pth', device = 'cuda:0'):
        self.config = yaml.load(open(config_path, 'r'), Loader=yaml.Loader)
        self.device = device
        self.model = self.init_model_with_checkpoint(checkpoint)
        self.tokenizer = BertTokenizer.from_pretrained(self.config['text_encoder'])
        self.transform = transforms.Compose([
                        transforms.Resize((self.config['image_res'], self.config['image_res']), interpolation=Image.BICUBIC),
                        transforms.ToTensor(),
                        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
    ])

    def init_model_with_checkpoint(self,checkpoint):
        print("Creating model")
        model = XVLM(config=self.config)
        model.load_pretrained(checkpoint, self.config, load_bbox_pretrain=True, is_eval=True)
        model = model.to(self.device)
        print("### Total Params: ", sum(p.numel() for p in model.parameters() if p.requires_grad))
        return model
    
    def visualize(self, image_path, text):
        rgb_img = Image.open(image_path).convert('RGB')
        W, H = rgb_img.size
        image = self.transform(rgb_img).unsqueeze(0)
        self.model.eval()
        image = image.to(self.device)
        text_input = self.tokenizer(text, padding='longest', return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs_coord = self.model(image, text_input.input_ids, text_input.attention_mask, target_bbox=None).cpu().detach().numpy()
        output_coord = outputs_coord[0]
        output_coord[[0,2]]*=W
        output_coord[[1,3]]*=H
        x,y,w,h = output_coord
        cv2_img = np.asarray(rgb_img)
        cv2_img = cv2.rectangle(cv2_img, (int(x-1/2*w), int(y-1/2*h)), (int(x + 1/2*w), int(y + 1/2*h)), (0, 255, 255), 2)
        print(text)
        plt.figure(figsize=(15,9))
        plt.imshow(cv2_img)
        plt.show()

    # input: image(ndarray, BGR), text
    # output: bbox(l,t,r,b)
    @torch.no_grad()
    def predict(self, image:np.ndarray, text:str):
        rgb_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        W, H = rgb_img.size
        image = self.transform(rgb_img).unsqueeze(0)
        self.model.eval()
        image = image.to(self.device)
        text_input = self.tokenizer(text, padding='longest', return_tensors="pt").to(self.device)
        outputs_coord = self.model(image, text_input.input_ids, text_input.attention_mask, target_bbox=None).cpu().detach().numpy()
        output_coord = outputs_coord[0]
        output_coord[[0, 2]] *= W
        output_coord[[1, 3]] *= H

        # [cx,cy,w,h] -> [l,t,r,b]
        output_coord[0] -= output_coord[2]/2
        output_coord[1] -= output_coord[3]/2
        output_coord[2] += output_coord[0]+1
        output_coord[3] += output_coord[1]+1
        return output_coord
