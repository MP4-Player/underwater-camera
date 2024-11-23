from gui import *
from board_defect.autopoint import *
from board_defect.main_code_board_defect import *

import cv2
import os 
import shutil
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates as sic
import json
import datetime
from board_defect.main_code_board_defect import *
from board_defect.autopoint import *
import numpy as np
from realsense2 import *

current_directory = os.getcwd()

def delete_pycache(directory):
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            dirs.remove('__pycache__') 

current_directory = os.getcwd()

def delete_pycache(directory):
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            dirs.remove('__pycache__') 

def main_menu(logo1_url, logo2_url):
    st.markdown(
    f"""
    <style>
    .header {{
        display: flex;
        text-align: left;
        justify-content: space-between;
        align-items: center;
    }}
    .logos {{
        display: flex;
        gap: 30px; /* Расстояние между логотипами */
        margin-right: 20px;
    }}
    .logo {{
        width: 80px; /* Укажите нужный размер логотипов */
    }}
    </style>
    <div class="header">
        <h1>Подводный измеритель размеров по камере</h1>
        <div class="logos">
            <img src="{logo1_url}" class="logo">
            <img src="{logo2_url}" class="logo">
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

    st.write("##### для ООО «Центр робототехники»")
    st.write("\n\t")
    st.write("""
            ### Назначение проекта
            Проекта предназначен для определения размеров трещин и пробоин в днищах кораблей и в причалах с использованием камеры находящееся подводой.
            """)
    st.write("## Инструкция по пользованию приложением")
    st.write("""
#### Главная страница.
- Ознакомьтесь с названием и назначением приложения.
- Убедитесь, что необходимое оборудование подключено.

#### Процесс измерения:
- Нажмите на кнопку **"Перейти к измерениям"** или на кнопку **"📏Измерение"** в боковой панели, чтобы перейти к основному функционалу.
- На странице измерений вы увидите основное окно, где будет видеострим с подводной камеры.
- Для приостановки видеострима нажмите на кнопку **"Пауза"**.
- После этого, перед вами будет изображение на котором нужно отметить 2 точки.
- Далее высветится окно с результатами измерения и окно с для ввода названия объекта.

#### Сохранение результатов:
- После завершения измерения сохраните результаты.
- Введите название объекта в поле "Название объекта"
- Нажмите кнопку **"Сохранить"**.
- Для измерения нового объекта нажмите 2 раза на кнопку **"Новый объект"** или кнопку   **"📏Измерение"** в боковой панели.

#### История измерений:
- Перейдите в раздел **"История измерений"** через боковую панель для просмотра ранее сохранённых данных.
- Вы можете просмотреть или удалить ненужные записи.

#### Обратная связь:
- Если у вас возникли вопросы или проблемы, ознакомьтесь с документацией представленной на главном экране.
""", key = 'text')
    # Кнопка
    st.write("\n\n")
    #st.button("Перейти к измерениям", key="measurement_button")
    
    if st.button("Перейти к измерениям"):
        st.session_state["page"] = "measurements"
        st.rerun()

def measurement_window():
    delete_pycache(current_directory)
    
    st.title('Трансляция камеры')
        
    if "paused" not in st.session_state:
        st.session_state["paused"] = False
    
    if 'points' not in st.session_state:
        st.session_state['points'] = []
    
    if 'flag' not in st.session_state:
        st.session_state['flag'] = True
    
    if 'flag' not in st.session_state:
        st.session_state['frame'] = []

    if 'flag' not in st.session_state:
        st.session_state['size'] = 0

    if 'realsense' not in st.session_state:
        st.session_state['realsense'] = DepthCamera(resolution_width, resolution_height)

    
    if st.session_state['flag'] == True:
        stream_realsense(st.session_state['flag'])
    
    size = st.session_state['size'] if 'size' in st.session_state.keys() else 0
    title_empty = st.empty()
    title = title_empty.text_input("Введите название объекта:", key = 'title')
    st.write(f"<h3 style='font-size:20px;'>Размер объекта: {size} мм</h3>", unsafe_allow_html=True)

    if st.button("Сохранить", key = 'save'):
        if identical_names(title) == 1:
            st.error (f"Объект {title} уже есть, пожалуйста, измените название объекта.")
            title_empty = st.empty()
            title = title_empty.text_input("Введите название объекта:", key = 'title_')
        else:
            save_object(title, st.session_state['size'])
            st.success("Объект успешно сохранен!")
        title_empty.empty()
        
    create_frame()
    

def create_file():
    data = {}

    with open('test.json', "w") as json_file:
        json.dump(data, json_file, indent=8)  
    return


def save_object(name, size):
    delete_pycache(current_directory)
    
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

def clear_text():
    st.session_state.text = ""


# def get_dots_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
def get_dots_coords(point):
    center = point
    radius = 3
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )
    
    
def create_frame():
    delete_pycache(current_directory)

    continue_button = st.button("Новый объект")
    
    img = Image.fromarray(st.session_state['frame'])
    draw = ImageDraw.Draw(img)
    
    for point in st.session_state["points"]:
        #(st.session_state["points"])
        coords = get_dots_coords(point)
        draw.ellipse(coords, fill="green")
            
    if not continue_button and len(st.session_state['points']) <= 2:
        value = sic(img, key="pil")
        if value is not None:
            point = value["x"], value["y"]
            if point not in st.session_state["points"]:
                new_point = mouse_callback(value['x'], value['y'], True, True, st.session_state["contours"])
                st.session_state["points"].append(new_point)
                if len(st.session_state['points']) == 3:
                    del st.session_state["points"][2]
                del st.session_state['pil']
                st.rerun()
        if len(st.session_state["points"]) == 2:
            dst = calc_dist(st.session_state["points_xyz"], st.session_state['points'])
            st.session_state["size"] = dst
        

    elif continue_button:
        del st.session_state["points"], st.session_state["frame"], st.session_state["flag"], st.session_state["paused"], st.session_state["size"]


def stream(flag):
    # Контейнер для отображения видео
    frame_placeholder = st.empty()

    # Кнопка "Пауза" отображается вне основного цикла
    button_placeholder = st.empty()
    if button_placeholder.button("Пауза" if not st.session_state["paused"] else "Продолжить"):
        st.session_state["paused"] = not st.session_state["paused"]

    if not st.session_state['paused'] or flag:
        # Захват видео с камеры
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("The video capture has ended.")
                break

            # Преобразуем цветной формат и отображаем поток
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame, contours = process_frame(frame)
            if not st.session_state['paused']:
                frame_placeholder.image(frame, channels="RGB", width=800)
            else:
                # Сохраняем текущий кадр при паузе
                st.session_state["frame"] = frame
                st.session_state["flag"] = False
                st.session_state["contours"] = contours
                break
        cap.release()
        cv2.destroyAllWindows()

def stream_realsense(flag):
    frame_placeholder = st.empty()
    button_placeholder = st.empty()

    if button_placeholder.button("Пауза" if not st.session_state["paused"] else "Продолжить"):
        st.session_state["paused"] = not st.session_state["paused"]
    print(st.session_state["paused"])
    

    if not st.session_state['paused'] or flag:
        try:
            depth_scale = st.session_state['realsense'].get_depth_scale()

            while True:
                ret, depth_raw_frame, color_raw_frame = st.session_state['realsense'].get_raw_frame()
                if not ret:
                    print("Unable to get a frame")
                    break

                rgb_image = np.asanyarray(color_raw_frame.get_data())
                depth_image = np.asanyarray(depth_raw_frame.get_data())
                frame = show(rgb_image, depth_image)
                frame, contours = process_frame(frame)
                print(st.session_state["paused"])
                if st.session_state['paused'] == False:
                    frame_placeholder.image(frame, channels="RGB", width=800)
                elif st.session_state['paused'] == True:
                    print("WE ARE IN ELIF")
                    if st.session_state['realsense']:
                        st.session_state['realsense'].release()
                    points_xyz = depth2PointCloud(depth_raw_frame, depth_scale)
                    st.session_state["frame"] = frame
                    st.session_state["points_xyz"] = points_xyz
                    st.session_state["flag"] = False
                    st.session_state["contours"] = contours
                    break
        except RuntimeError as e:
            st.error(f"Error: {e}. Please make sure the device is not busy and try again.")
            


    
if __name__ == '__main__':
    delete_pycache(current_directory)
    
    logo1_url = "https://static.tildacdn.com/tild6233-3463-4638-b538-316661656262/Group_277132226.svg"
    logo2_url = "https://lh5.googleusercontent.com/proxy/m--gX8s53PHjWyQu2N9hzN6nxVDua3KVbvWJbRWYKrXsSesft3S16ZN04mokdzZf5djYegQG-vxagH_8HsS8IntftnzMAUyFl61kKt2KggURRzcLIA"
    try:
        with open('test.json', "r") as json_file:
            pass
    except FileNotFoundError:
        create_file()

    with open('test.json') as f:
        objects_list = json.load(f)

    with st.sidebar:
        if st.button("🏠 Главная страница", key="home-button", help="Нажмите, чтобы перейти на главную страницу"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
            

        if st.button("📏 Измерение",  key="measuring-button", help="Нажмите, чтобы начать измерение объектов"):
            st.session_state.text = ''
            st.session_state["page"] = "measurements"
            st.rerun()
        
        object_name = st.selectbox("⏱️ История измерения", list(objects_list.keys()))
        if object_name in objects_list:  
            st.sidebar.write(f"Размер объекта: {object_name}")
            object_list = objects_list[object_name]
            st.sidebar.write(f"- Время: {object_list['time']}")
            st.sidebar.write(f"- Размер: {object_list['size']}")
            
        if st.button("🗑️ Удалить историю", key="delete-history-button", help="Нажмите, чтобы очистить историю", type = "secondary"):
            create_file()
            st.success("История успешно удалена.")

    if "page" not in st.session_state:
        st.session_state["page"] = "main"

    if st.session_state["page"] == "main": # вызов главного меню
        main_menu(logo1_url, logo2_url)
        
    elif st.session_state["page"] == "measurements": # Вызов рабочего пространства
        measurement_window()