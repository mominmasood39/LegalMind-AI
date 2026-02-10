import google.generativeai as genai

genai.configure(api_key="AIzaSyCd0MhfMWTZiu6zSL2r0_NyXDlq6CylX20")

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)