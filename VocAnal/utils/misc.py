import os
import errno
from base64 import b64encode
from wordcloud import WordCloud
from VocAnal import app
from VocAnal.classes.Pdf import PdfHandler
from VocAnal.utils.constants import ALLOWED_EXTENSIONS


def allowed_file(filename):
    """
    Validate the filename
    :param filename: str
    :return: bool
    """
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(stream_in):
    """
    Convert a PDF byte stream into str
    :param stream_in: bytes
    :return: str
    """
    converter = PdfHandler(stream_in)
    corpus = converter.get_corpus()
    return corpus


def get_project_name(file_path):
    """
    Given a file path return a string
    corresponding to the base name
    witthout the extension
    :param file_path: str
    :return: str
    """
    base_name = os.path.basename(file_path)
    try:
        proj_name = os.path.splitext(base_name)[0]
    except IndexError:
        proj_name = base_name
    return proj_name


def create_nonexistent_dir(path, exc_raise=False):
    """
    Create a directory from a given path if it does not exist.
    If exc_raise is False, no exception is raised

    """
    try:
        os.makedirs(path)
        app.logger.debug("Created directory with path: {}".format(path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            app.logger.exception(
                "Could not create directory with path: {}".format(path))
            if exc_raise:
                raise


def save_wordcloud(corpus, out_dir_name):
    """
    Save wordcloud basic image
    :param corpus: str: the string of the
        document content
    :param out_dir_name: str: output directory
    :return: None
    """
    app.logger.debug("Making Word Cloud image")
    wc = WordCloud(
        width=800,
        height=600,
        background_color="black",
        contour_width=3,
        contour_color="steelblue"
    )
    wc.generate(corpus)
    output_fp = os.path.join(out_dir_name, "wordcloud.png")
    wc.to_file(output_fp)


def b64str_from_path(path):
    """
    Return a base64 image from a given path
    :param path: str
    :return: str
    """
    try:
        with open(path, "rb") as img_file:
            img_bytes = img_file.read()
        img_str = b64encode(img_bytes).decode('utf-8')
        return img_str
    except Exception as e:
        app.logger.error(e)
        return e
