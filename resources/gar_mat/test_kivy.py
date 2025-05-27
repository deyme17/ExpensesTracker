import matplotlib.pyplot as plt
from backend_kivyagg import FigureCanvasKivyAgg
from backend_kivy import NavigationToolbar2Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class MatplotlibKivyApp(App):
    def build(self):
        # Create a basic BoxLayout
        layout = BoxLayout(orientation='vertical')

        # Create a matplotlib figure and plot something
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
        ax.set_title('Simple Plot')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')

        # Wrap the figure in a Kivy widget
        canvas = FigureCanvasKivyAgg(fig)
        #toolbar = NavigationToolbar2Kivy(canvas)
        #layout.add_widget(toolbar)
        layout.add_widget(canvas)
        return layout

if __name__ == '__main__':
    MatplotlibKivyApp().run()

