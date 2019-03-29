import os
import cv2
import json
import pydicom
import numpy as np
from PIL import Image
from fpdf import FPDF
from datetime import datetime

def convert2image(ds, name):
    shape = ds.pixel_array.shape
    image_2d = ds.pixel_array.astype(float)
    image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0
    image_2d_scaled = np.uint8(image_2d_scaled)
    im = Image.fromarray(image_2d_scaled)
    im.save('../test/'+name[:-4]+'.png')
    return ds.pixel_array


def dicom2dict(x,fin,imp,tags):
    dcm_data = {}
    dcm_data['PatientName'] = str(x.PatientName)
    dt = datetime.strptime(str(x.PatientBirthDate)[:4]+" "+str(x.PatientBirthDate[4:6])+" "+str(x.PatientBirthDate)[6:], '%Y %m %d')
    dcm_data['DOB'] = dt.strftime("%d %B %Y")
    dcm_data['Physician'] = str(x.ReferringPhysicianName)
    dcm_data['Exam'] = str(x.BodyPartExamined)+ " " + str(x.Modality)

    dt = datetime.strptime(str(x.StudyDate)[:4]+" "+str(x.StudyDate[4:6])+" "+str(x.StudyDate)[6:], '%Y %m %d')
    dcm_data['ExamDate'] = dt.strftime("%d %B %Y")
    dcm_data['CH'] = str(x.ReasonForTheRequestedProcedure)
    dcm_data['Findings'] = fin
    dcm_data['Impression'] = imp
    dcm_data['Tags'] = tags
    
    return dcm_data


#pending - include header and footer. Include AGMIR logo
def generate_medical_report(image_file,dcm_file_data):
    pdf = FPDF(format='letter', unit='in')

    effective_page_width = pdf.w - 2*pdf.l_margin
    pdf.add_page()

    #Header
    pdf.set_font('Times','B',14.0)
    pdf.cell(1.0, 0.0,"Radiology Report",ln=1, align="C")
    pdf.ln(0.5)
    
    #Patient Demographic
    pdf.set_font('Times','',10.0) 
    pdf.cell(1.0, 0.0, "Patient Name: "+str(dcm_file_data['PatientName']), ln=1, align="L")
    pdf.ln(0.25)
    
    pdf.cell(1.0, 0.0, txt="Date of Birth: "+str(dcm_file_data['DOB']), ln=1, align="L")
    pdf.ln(0.25)
    
    pdf.cell(1.0, 0.0, txt="Physician: "+str(dcm_file_data['Physician']), ln=1, align="L")
    pdf.ln(0.25)
    
    pdf.cell(1.0, 0.0, txt="Exam: "+str(dcm_file_data['Exam']), ln=1, align="L")
    pdf.ln(0.25)
    
    pdf.cell(1.0, 0.0, txt="Date: "+str(dcm_file_data['ExamDate']), ln=1, align="L")
    pdf.ln(0.5)
    
    #Clinical Information
    pdf.set_font('Times','B',10.0)
    pdf.cell(1.0, 0.0, txt="Clinical History ", ln=1, align="L")
    pdf.set_font('Times','',10.0)
    Clinical_History = str(dcm_file_data['CH'])
    pdf.ln(0.25)
    pdf.multi_cell(effective_page_width*0.8, .15,Clinical_History)
    pdf.ln(0.25)
    
    #Comparison
    #pdf.set_font('Times','B',10.0)
    #pdf.cell(1.0, 0.0, txt="Comparison", ln=1, align="L")
    #Comparison = str(dcm_file_data['Comp'])
    #pdf.ln(0.25)
    #pdf.set_font('Times','',10.0)
    #pdf.multi_cell(effective_page_width, .15,Comparison)
    #pdf.ln(0.25)
    
    #Technique
    #pdf.set_font('Times','B',10.0)
    #pdf.cell(1.0, 0.0, txt="Technique", ln=1, align="L")
    #pdf.ln(0.25)
    #Technique = str(dcm_file_data['Technique'])
    #pdf.set_font('Times','',10.0)
    #pdf.multi_cell(effective_page_width, .15,Technique)
    #pdf.ln(0.25)
    
    #Findings
    pdf.set_font('Times','BI',10.0)
    pdf.cell(1.0, 0.0, txt="Findings", ln=1, align="L")
    pdf.ln(0.25)
    Findings = str(dcm_file_data['Findings'])
    pdf.set_font('Times','',10.0)
    pdf.multi_cell(effective_page_width, .15,Findings)
    pdf.ln(0.25)
    
    #Impression
    pdf.set_font('Times','B',10.0)
    pdf.cell(1.0, 0.0, txt="Impression", ln=1, align="L")
    pdf.ln(0.25)
    Impression = str(dcm_file_data['Impression'])
    pdf.set_font('Times','',10.0)
    pdf.multi_cell(effective_page_width, .15,Impression)
    pdf.ln(0.25)
    
    #Tags
    pdf.set_font('Times','B',10.0)
    pdf.cell(1.0, 0.0, txt="Tags", ln=1, align="L")
    pdf.ln(0.25)
    Tags = str(dcm_file_data['Tags'])
    pdf.set_font('Times','',10.0)
    pdf.multi_cell(effective_page_width, .15,Tags)
    pdf.ln(0.25)
    filename = str(image_file) +'.pdf'
    pdf.output(filename)
    
    
if __name__ == "__main__":
    print ("Hello World")
