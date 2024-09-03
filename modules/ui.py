from flet import Container, Column, Row, Text, Stack, colors as COLORS
import flet as ft
from random import randint
from time import time
from .globals import MyColors, gTaskList, writeFile


class GlobalMonitor(Row):
    def __init__(self):
        super().__init__(
            controls=[
                TaskSelector(),
                TaskManager()
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

class TaskSelector(Container):
    def __init__(self):
        super().__init__(
            content=Column(
                controls=[
                    Container( #Button
                        content=Text("Select Random Task"),
                        bgcolor=COLORS.GREY_900,
                        padding=12,
                        border_radius=8,
                        on_click=self.selectTask,
                    ),
                    Container(
                        content=Text(size=48, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        expand=True,
                        alignment=ft.alignment.center,
                        border_radius=20,
                        margin=20,
                        padding=20,
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=MyColors.ULTRAGREY,
            padding=12,
            border_radius=8,
            width=500,
        )
        
    def selectTask(self, e):
        task_pool = [task for task in gTaskList if "[x]" not in task]
        selected_task = 0
        start_time = time()
        self.content.controls[1].bgcolor = None
        while time()-start_time < 1:
            if not len(task_pool): 
                self.content.controls[1].content.value = "All clear! Create new task!"
                break
            e.control.on_click = None
            selected_task = task_pool[randint(0, len(task_pool)-1)]
            self.content.controls[1].content.value = selected_task[4:]
            self.update()
            if len(task_pool) == 1: break
        e.control.on_click = self.selectTask
        self.content.controls[1].bgcolor = COLORS.GREY_900 if len(task_pool) else COLORS.GREEN_900
        self.update()

class TaskManager(Container):
    def __init__(self):
        super().__init__(
            content=Column(
                controls=[
                    Column(
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    Container(
                        content=Text("+"),
                        alignment=ft.alignment.center,
                        padding=12,
                        bgcolor=MyColors.ULTRAGREY,
                        border=ft.border.all(2, COLORS.GREY_800),
                        on_click=self.addTask,
                    )
                ],
            ),
            expand=True,
            margin=12,
        )

        for i, x in enumerate(gTaskList):
            self.content.controls[0].controls.append(TaskBlock(i, x, self.deleteTask))
    
    def addTask(self, e):
        gTaskList.append("[ ] ")
        print(gTaskList)
        self.content.controls[0].controls.append(TaskBlock(len(gTaskList)-1, gTaskList[-1], self.deleteTask))
        writeFile(gTaskList)
        self.update()
        self.content.controls[0].controls[-1].content.controls[1].focus()

    def deleteTask(self, e):
        idx = e.control.data
        gTaskList.pop(idx)
        self.content.controls[0].controls.pop(idx)
        writeFile(gTaskList)
        for i, x in enumerate(self.content.controls[0].controls[idx:]):
            x.updateTaskIdx(idx+i)
        self.update()

class TaskBlock(Container):
    def __init__(self, task_idx, task, deleteFunction):
        self.task = task
        self.task_idx = task_idx
        super().__init__(
            content=Row(
                controls=[
                    ft.Checkbox(
                        on_change=self.checkToggle,
                        check_color=COLORS.BLACK54,
                        fill_color={ft.ControlState.SELECTED: COLORS.WHITE30}
                    ),
                    ft.TextField(
                        value=task[4:] if len(task) > 4 else "", 
                        expand=True, 
                        border_color=COLORS.TRANSPARENT, 
                        focused_border_color=COLORS.WHITE,
                        on_change=self.alter_task,
                    ),
                    Container(
                        content=ft.Icon(ft.icons.DELETE, color=COLORS.WHITE10),
                        on_click=deleteFunction,
                        data=self.task_idx,
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=COLORS.GREY_900,
            padding=8,
            border_radius=4,
        )

        self.setState("[x]" in task)

    def setState(self, state):
        checkbox = self.content.controls[0]
        textfield : ft.TextField = self.content.controls[1]
        if state:
            checkbox.value = state
            self.bgcolor = None
            textfield.text_style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH,
                decoration_color=COLORS.WHITE30,
                color=COLORS.WHITE30
            )
            gTaskList[self.task_idx] = "[x]" + gTaskList[self.task_idx][3:]
        else:
            self.bgcolor = COLORS.GREY_900
            self.content.controls[1].text_style = None
            gTaskList[self.task_idx] = "[ ]" + gTaskList[self.task_idx][3:]
    
    def checkToggle(self, e):
        self.setState(e.control.value)
        self.update()
    
    def alter_task(self, e):
        gTaskList[self.task_idx] = gTaskList[self.task_idx][:4] + e.control.value
        writeFile(gTaskList)

    def updateTaskIdx(self, idx):
        self.task_idx = idx
        self.content.controls[2].data = idx
        self.update()