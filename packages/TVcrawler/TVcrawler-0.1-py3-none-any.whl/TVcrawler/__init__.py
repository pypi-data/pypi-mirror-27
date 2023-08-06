import sys, subprocess

class Endpoints():
    base = "https://oneom.tk"
    fresh = base + "/ep"
    def show(self, id):
        return self.base + "/serial/" + str(id)

    def episode(self, id):
        return self.base + "/ep/" + str(id)

    def search(self, title):
        return self.base + "/search/serial?title=" + str(title)


def open_magnet(magnet):
        """Open magnet according to os."""
        if sys.platform.startswith('linux'):
            subprocess.Popen(['xdg-open', magnet],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif sys.platform.startswith('win32'):
            os.startfile(magnet)
        elif sys.platform.startswith('cygwin'):
            os.startfile(magnet)
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', magnet],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.Popen(['xdg-open', magnet],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
