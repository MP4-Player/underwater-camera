import cv2
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates as sic
import json
import datetime
from board_defect.main import *
from board_defect.autopoint import *

def create_file():
    data = {}

    with open('test.json', "w") as json_file:
        json.dump(data, json_file, indent=8)
        
    return

def save_object(name, size):
    
    today = datetime.datetime.today()
    new_object = {
        "time": str(today.strftime("%d/%m/%Y %H:%M:%S")),
        "size": size
    }
    
    data = json.load(open("test.json"))
    data[name] = new_object
    
    with open('test.json', "w") as json_file:
        json.dump(data, json_file, indent=4)
        
    return


def identical_names(name):
    with open('test.json') as f:
        json_list = json.load(f)
        
    if name in json_list:
        return 1

def get_dots_coords(point):
    center = point
    # print(center)
    radius = 4
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )

def create_frame():
    #st.session_state['flag']
    continue_button = st.button("New object")
    
    if not continue_button and len(st.session_state['points']) <= 2:
        img = Image.fromarray(st.session_state['frame'])
        draw = ImageDraw.Draw(img)
        
        
        for point in st.session_state["points"]:
            print(st.session_state["points"])
            coords = get_dots_coords(point)
            draw.ellipse(coords, fill="red")
        
        value = sic(img, key="pil")
        # print(value)
        if value is not None:
            point = value["x"], value["y"]
            # print(point)
            if point not in st.session_state["points"]:
                st.session_state["points"].append(point)
                st.rerun()
        else:
            pass
    
    elif continue_button:
        del st.session_state["points"], st.session_state["frame"], st.session_state["flag"]#, st.session_state['pil']
        print(st.session_state)

def stream(flag):
    paused_button = st.button("Paused")
    
    if not paused_button or flag:
        # cap = freenect.sync_get_video()[0]
        cap = cv2.VideoCapture(0)
        frame_placeholder = st.empty()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("The video capture has ended.")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            
            frame = process_frame(frame)
            if not paused_button:
                frame_placeholder.image(frame, channels="BGR", width=800)
            
            if paused_button:
                st.session_state['flag'] = False
                st.session_state['frame'] = frame
                break
    
    
    cv2.destroyAllWindows()

    
if __name__ == '__main__':
    
    try:
        with open('test.json', "r") as json_file:
            pass
    except FileNotFoundError:
        create_file()

    with open('test.json') as f:
        objects_list = json.load(f)

    st.sidebar.title('История измерений')

    with st.sidebar:
        if st.button("Удалить историю", key = 'delete'):
            create_file()
            st.success("История успешно удалена.")
        object_name = st.selectbox("Сохраненные объекты", list(objects_list.keys()))


    if object_name in objects_list:  
        st.sidebar.write(f"Размер объекта: {object_name}")
        object_list = objects_list[object_name]
        st.sidebar.write(f"- Время: {object_list['time']}")
        st.sidebar.write(f"- Размер: {object_list['size']}")

    st.title('Окно камеры')
    
    if 'points' not in st.session_state:
        st.session_state['points'] = []
    
    if 'flag' not in st.session_state:
        st.session_state['flag'] = True
    
    if 'flag' not in st.session_state:
        st.session_state['frame'] = []

    
    if st.session_state['flag'] == True:
        frame_main = stream(st.session_state['flag'])
        
    create_frame()
    
    title = st.text_input("Введите название объекта:", key = 'title')
    size = 4539

    identical_names(title)

    if st.button("Сохранить", key = 'save'):
        if identical_names(title) == 1:
            st.error (f"Объект {title} уже есть, пожалуйста, измените название объекта.")
        else:
            save_object(title, size)
            st.success("Объект успешно сохранен!")