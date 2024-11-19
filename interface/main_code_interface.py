import cv2
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates as sic
import json
import datetime
from board_defect.main_code_board_defect import *
from board_defect.autopoint import *

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

    # Подзаголовок
    st.write("##### для ООО «Центр робототехники»")

    # Инструкция
    st.write("## Инструкция по пользованию приложением")
    st.write("""
    #### Главная страница:
    - Ознакомьтесь с названием и назначением приложения.
    - Убедитесь, что необходимое оборудование подключено.

    #### Переход к измерениям:
    - Нажмите на кнопку **"Перейти к измерениям"**, чтобы перейти к основному функционалу.

    #### Процесс измерения:
    - На странице измерений настройте параметры для работы устройства:
    - Выберите параметры камеры (разрешение, угол обзора и т. д.).
    - Убедитесь, что устройство корректно откалибровано.
    - Нажмите кнопку **"Начать измерение"**, чтобы получить данные.

    #### Сохранение результатов:
    - После завершения измерения сохраните результаты:
    - Нажмите кнопку **"Сохранить"**.
    - Укажите путь для сохранения файла или выберите предложенный.

    #### История измерений:
    - Перейдите в раздел **"История измерений"** через боковую панель для просмотра ранее сохранённых данных.
    - Вы можете скачать результаты или удалить ненужные записи.

    #### Анализ данных:
    - Используйте инструменты анализа внутри приложения для обработки измерений.
    - Сравните результаты с предыдущими измерениями для получения полной картины.

    #### Обратная связь:
    - Если у вас возникли вопросы или проблемы, обратитесь в техническую поддержку или ознакомьтесь с документацией.
    """, key = 'text')
    # Кнопка
    st.write("\n\n")
    #st.button("Перейти к измерениям", key="measurement_button")
    
    if st.button("Перейти к измерениям"):
        st.session_state["page"] = "measurements"
        st.rerun()

def measurement_window():
    
    st.title('Трансляция камеры')
        
    if "paused" not in st.session_state:
        st.session_state["paused"] = False
    
    if 'points' not in st.session_state:
        st.session_state['points'] = []
    
    if 'flag' not in st.session_state:
        st.session_state['flag'] = True
    
    if 'flag' not in st.session_state:
        st.session_state['frame'] = []

    
    if st.session_state['flag'] == True:
        stream(st.session_state['flag'])
    
    title = st.text_input("Введите название объекта:", key = 'title')
    size = 4539

    identical_names(title)

    if st.button("Сохранить", key = 'save'):
        if identical_names(title) == 1:
            st.error (f"Объект {title} уже есть, пожалуйста, измените название объекта.")
        else:
            save_object(title, size)
            st.success("Объект успешно сохранен!")
        
    create_frame()
    



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

def clear_text():
    st.session_state.text = ""

def get_dots_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    print(center)
    radius = 4
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )
    
    
def create_frame():
    continue_button = st.button("Новый объект")
    
    if not continue_button and len(st.session_state['points']) <= 2:
        img = Image.fromarray(st.session_state['frame'])
        draw = ImageDraw.Draw(img)
        
        
        for point in st.session_state["points"]:
            print(st.session_state["points"])
            coords = get_dots_coords(point)
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
    
    elif continue_button:
        del st.session_state["points"], st.session_state["frame"], st.session_state["flag"], st.session_state["paused"]#, st.session_state['pil']
        print(st.session_state)


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
            frame = process_frame(frame)
            if not st.session_state['paused']:
                frame_placeholder.image(frame, channels="RGB", width=800)
            else:
                # Сохраняем текущий кадр при паузе
                st.session_state["frame"] = frame
                st.session_state["flag"] = False
                break
        cap.release()
        cv2.destroyAllWindows()


    
if __name__ == '__main__':
    
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