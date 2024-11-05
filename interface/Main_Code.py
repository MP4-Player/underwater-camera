import cv2
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates as sic
import json
import datetime

def create_file():
    empty_data = {}

    with open('test.json', "w") as json_file:
        json.dump(empty_data, json_file, indent=8)
        
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


def the_same(name):
    with open('test.json') as f:
        json_list = json.load(f)
        
    if name in json_list:
        return 1
      
def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    print(center)
    radius = 4
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )
    
def Frame():
    #st.session_state['flag']
    Continuation = st.button("New object")
    
    if not Continuation and len(st.session_state['points']) <= 2:
        img = Image.fromarray(st.session_state['frame'])
        draw = ImageDraw.Draw(img)
        
        
        for point in st.session_state["points"]:
            print(st.session_state["points"])
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill="red")
        
        value = sic(img, key="pil")
        print(value)
        if value is not None:
            point = value["x"], value["y"]
            print(point)
            if point not in st.session_state["points"]:
                st.session_state["points"].append(point)
                st.rerun()
        else:
            pass
    
    elif Continuation:
        del st.session_state["points"], st.session_state["frame"], st.session_state["flag"]#, st.session_state['pil']
        print(st.session_state)

def Stream(flag):
    Paused_button = st.button("Paused")
    
    if not Paused_button or flag:
        cap = cv2.VideoCapture(0)
        frame_placeholder = st.empty()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("The video capture has ended.")
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if not Paused_button:
                frame_placeholder.image(frame, channels="RGB", width=800)
            
            if Paused_button:
                st.session_state['flag'] = False
                st.session_state['frame'] = frame
                break
    
    cap.release()
    cv2.destroyAllWindows()

    
if __name__ == '__main__':
    
    try:
        with open('test.json', "r") as json_file:
            pass
    except FileNotFoundError:
        create_file()

    with open('test.json') as f:
        task_list = json.load(f)

    st.sidebar.title('История измерений')

    with st.sidebar:
        if st.button("Удалить историю", key = 'delete'):
            create_file()
            st.success("История успешно удалена.")
        task_name = st.selectbox("Сохраненные объекты", list(task_list.keys()))


    if task_name in task_list:  
        st.sidebar.write(f"Размер объекта: {task_name}")
        task = task_list[task_name]
        st.sidebar.write(f"- Время: {task['time']}")
        st.sidebar.write(f"- Размер: {task['size']}")

    st.title('Окно камеры')
    
    if 'points' not in st.session_state:
        st.session_state['points'] = []
    
    if 'flag' not in st.session_state:
        st.session_state['flag'] = True
    
    if 'flag' not in st.session_state:
        st.session_state['frame'] = []

    
    if st.session_state['flag'] == True:
        frame_main = Stream(st.session_state['flag'])
        
    Frame()
    
    title = st.text_input("Введите название объекта:", key = 'title')
    size = 4539

    the_same(title)

    if st.button("Сохранить", key = 'save'):
        if the_same(title) == 1:
            st.error (f"Объект {title} уже есть, пожалуйста, измените название объекта.")
        else:
            save_object(title, size)
            st.success("Объект успешно сохранен!")