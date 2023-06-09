import click
import os
import datetime
from collections import defaultdict
import shutil

OSSLINK = "http://zhouhao-blog.oss-cn-shanghai.aliyuncs.com/Blog/articles/"
HEXOPATH = os.path.expanduser("~/Blog/source/_posts")
COVERLINK = "http://zhouhao-blog.oss-cn-shanghai.aliyuncs.com/Blog/cover"

MTEMPLATE = defaultdict(str)


def gain_curdate():
    cur_date = datetime.datetime.now()
    return cur_date.strftime('%Y-%m-%d %H:%M:%S')


def init_template():
    MTEMPLATE['katex'] = 'true'
    MTEMPLATE['date'] = gain_curdate()
    MTEMPLATE['cover'] = COVERLINK


def create_metadata_string(template):
    metadata_str = '---\n'
    for key, value in template.items():
        if isinstance(value, list):
            metadata_str += f'{key}:\n'
            metadata_str += '\n'.join([f'  - {item}' for item in value])
            if len(value) > 0:
                metadata_str += '\n'
        else:
            metadata_str += f'{key}: {value}\n'
    metadata_str += '---\n'
    return metadata_str


def upload_assets(md_name):
    """
    By default, the folder for uploading is the concatenated name
    of the Markdown file you want to operate on,
    followed by the suffix 'asserts'. The program will search for this folder
    in the current directory, and if the folder is not found,
    an error will be raised.
    # For example:
        # demo.md      -> your markdown file name
        # demo.asserts -> this direcoty will be upload to your oss
    """
    name, _ = os.path.splitext(md_name)
    res_path = os.path.join(OSSLINK, f'{name}.asserts')
    print(f"oss mkdir {res_path}")


def replacelink(file_path, old_str, new_str):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Replace the old string with the new string
    new_content = file_content.replace(old_str, new_str)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(new_content)


def copy_to_hexo_path(input_file):
    filename = os.path.basename(input_file)
    destination = os.path.join(HEXOPATH, filename)
    shutil.copy2(input_file, destination)


@click.command()
@click.option('--input_file', '-f', prompt="Markdown file path", help='Input your markdown file')
@click.option('--title', '-t', prompt='Title', help='Article title')
@click.option('--categories', '-c', prompt="Categories", help='Hexo Categories')
@click.option('--tag', '-g', prompt='Tag', help='Article Tags')
def user_format(input_file, title, categories, tag):
    assert (os.path.exists(input_file))
    MTEMPLATE["categories"] = categories
    MTEMPLATE["title"] = title
    MTEMPLATE["tag"] = tag.split(',')
    metadata_str = create_metadata_string(MTEMPLATE)

    # Read the contents of the input_file
    with open(input_file, 'r') as f:
        content = f.read()

    # Add metadata to the beginning of the content
    new_content = metadata_str + content

    # Get the filename from the input_file path
    filename = os.path.basename(input_file)

    # Check if the destination file already exists in HEXOPATH
    destination = os.path.join(HEXOPATH, filename)
    if os.path.exists(destination):
        raise FileExistsError(
            f"The file '{filename}' already exists in HEXOPATH.")

    # Write the new_content to the destination file in HEXOPATH
    with open(destination, 'w') as f:
        f.write(new_content)


if __name__ == "__main__":
    init_template()
    user_format()
