import os
import argparse
import json
import re
import mmap
import time
import base64
import urllib.parse
import pkgutil
import importlib
import re
import encode_class
import colorama



CONFIG_FILE = 'config.json'
CLASSES = []

def read_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
                else:
                    print(f"警告：配置文件 {CONFIG_FILE} 为空，将使用默认配置。")
        except json.JSONDecodeError:
            print(f"警告：配置文件 {CONFIG_FILE} 格式不正确，将使用默认配置。")
    else:
        print(f"警告：配置文件 {CONFIG_FILE} 不存在，将创建新的配置文件。")
    
    # 使用默认配置
    default_config = {'patterns': []}
    write_config(default_config)
    return default_config

def write_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def add_patterns(new_patterns):
    config = read_config()
    existing_patterns = config.get('patterns', [])
    for pattern in new_patterns:
        if pattern not in existing_patterns:
            existing_patterns.append(pattern)
    config['patterns'] = existing_patterns
    write_config(config)
    return existing_patterns

def generate_flag_patterns(patterns):
    all_patterns = []
    for pattern in patterns:
        encoded = encode_text(pattern)
        all_patterns.extend(encoded)
    return list(set(all_patterns))

def filter_printable_chars(input_bytes):
    return ''.join(chr(c) for c in input_bytes if 32 <= c <= 126)

def search_flag_in_file(file_path, regex_pattern):
    matches = []
    try:
        pattern = re.compile(regex_pattern.encode('utf-8'),re.IGNORECASE)
        with open(file_path, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            for line_num, line in enumerate(iter(mm.readline, b""), 1):
                filtered_line = filter_printable_chars(line)
                for match in pattern.finditer(filtered_line.encode('utf-8')):
                    matched_text = match.group().decode('utf-8')
                    matches.append((line_num, filtered_line.strip(), matched_text))
    except Exception as e:
        print(f'错误：无法读取或处理文件 {file_path}: {str(e)}')
    return matches



def get_all_files(path):
    if os.path.isfile(path):
        yield path
    else:
        for root, _, files in os.walk(path):
            for file in files:
                if not file.endswith(('.py', 'output.txt')):
                    yield os.path.join(root, file)

def encode_text(text):
    if not isinstance(text, str):
        text = str(text)
    hex_encode = text.encode('utf-8').hex()
    hex_encode_x = ''.join([f'\\x{c:02x}' for c in text.encode('utf-8')])
    url_encode = urllib.parse.quote(text)
    unicode_encode = ''.join([f'\\u{ord(c):04x}' for c in text])
    ascii_encode = ' '.join(str(ord(c)) for c in text)
    ascii_encode_no_space = ''.join(str(ord(c)) for c in text)
    html_ascii_encode = ''.join([f'&#{ord(c)};' for c in text])

    base64_encode = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    

    return [
        text,
        hex_encode,
        hex_encode_x,
        url_encode,
        unicode_encode,
        ascii_encode,
        ascii_encode_no_space,
        html_ascii_encode,
        base64_encode
    ]

def load_encoders():
    global CLASSES
    for importer, modname, ispkg in pkgutil.iter_modules(encode_class.__path__):
        if modname != 'BaseEncoder':  # 跳过BaseEncoder
            module = importlib.import_module(f'encode_class.{modname}')
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if (isinstance(attribute, type) and 
                    issubclass(attribute, encode_class.BaseEncoder) and 
                    attribute != encode_class.BaseEncoder):
                    CLASSES.append(attribute())
                    
def show_encoders():
    print("已加载的编码器：")
    for encoder in CLASSES:
        print(f"- {encoder.name}: {encoder.description}")
    print("您可以自定义自己需要的编码器，编码器需要继承BaseEncoder类，并实现encode和decode方法")

def delete_patterns(patterns_to_delete):
    config = read_config()
    existing_patterns = config.get('patterns', [])
    for pattern in patterns_to_delete:
        if pattern in existing_patterns:
            existing_patterns.remove(pattern)
    config['patterns'] = existing_patterns
    write_config(config)
    return existing_patterns

def add_match_keywords(new_keywords):
    config = read_config()
    existing_keywords = config.get('match', [])
    for keyword in new_keywords:
        if keyword not in existing_keywords:
            existing_keywords.append(keyword)
    config['match'] = existing_keywords
    write_config(config)
    return existing_keywords

def delete_match_keywords(keywords_to_delete):
    config = read_config()
    existing_keywords = config.get('match', [])
    for keyword in keywords_to_delete:
        if keyword in existing_keywords:
            existing_keywords.remove(keyword)
    config['match'] = existing_keywords
    write_config(config)
    return existing_keywords

def search_file(file_path, keywords):
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                for keyword in keywords:
                    if keyword in line:
                        results.append({
                            'file_path': file_path,
                            'line_num': line_num,
                            'line_content': line.strip(),
                            'match_result': keyword,
                            'match_format': 'plain text',
                            'encoder': 'None'
                        })
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {str(e)}")
    return results

def show_logo():
    logo = """
    
    ______    __     ___    ______           ______    _                __              
   / ____/   / /    /   |  / ____/          / ____/   (_)   ____   ____/ /  ___    _____
  / /_      / /    / /| | / / __           / /_      / /   / __ \ / __  /  / _ \  / ___/
 / __/     / /___ / ___ |/ /_/ /          / __/     / /   / / / // /_/ /  /  __/ / /    
/_/       /_____//_/  |_|\____/          /_/       /_/   /_/ /_/ \__,_/   \___/ /_/     
                                                                                        
"""
    print(colorama.Fore.CYAN + logo)
    print(colorama.Fore.YELLOW + " "*70 +"- V 1.0.0 By: SakuraRabbit|云隐")
    print(colorama.Fore.YELLOW + " "*70 +"- Github:https://github.com/SakuraRabbit18/FlagFinder")
    print(colorama.Fore.YELLOW + " "*70 +"- 更多请关注云隐安全公众号")
    print(colorama.Fore.YELLOW + "Usage: python finder.py <path> [-o output] [-p pattern] [--add add] [--del delete] [--show-encoders] [--match] [--add-match add-match] [--del-match del-match]")
    print(colorama.Fore.YELLOW + "Example: python finder.py hack.pacp -o result.txt")
    print(colorama.Style.RESET_ALL)

def main():
    show_logo()
    parser = argparse.ArgumentParser(description='搜索文件中的flag')
    parser.add_argument('path', nargs='?', help='要搜索的文件或文件夹路径')
    parser.add_argument('-o', '--output', help='指定输出文件路径')
    parser.add_argument('-p', '--pattern', nargs='+', help='指定匹配词，指定匹配词后将使用当前匹配词不再读取配置文件，可以用空格分隔多个匹配词')
    parser.add_argument('--add', nargs='+', help='添加新的匹配词到配置文件')
    parser.add_argument('--del', '--delete', nargs='+', dest='delete', help='删除指定的匹配词')
    parser.add_argument('--show-encoders', action='store_true', help='显示已加载的编码器')
    parser.add_argument('-m', '--match',action='store_true',help='以匹配关键字搜索，该模式不再尝试解码')
    parser.add_argument('--add-match', nargs='+', help='添加新的匹配关键字到配置文件')
    parser.add_argument('--del-match', nargs='+', help='从配置文件中删除指定的匹配关键字')

    args = parser.parse_args()
    search_path = args.path
    output_file = args.output
    
    load_encoders()
    if args.show_encoders:
        show_encoders()
        return

    # 读取配置
    config = read_config()
    patterns = config.get('patterns', [])
    match_keywords = config.get('match', [])

    # 如果指定了新的模式，添加它们
    if args.add:
        patterns = add_patterns(args.add)
        print(f"添加匹配词: {args.add}")
        print(f"当前匹配词: {patterns}\n")
        exit()
    if args.delete:
        patterns = delete_patterns(args.delete)
        print(f"删除匹配词: {args.delete}")
        print(f"当前匹配词: {patterns}\n")
        exit()

    # 如果指定了新的匹配关键字，添加它们
    if args.add_match:
        match_keywords = add_match_keywords(args.add_match)
        print(f"添加匹配关键字: {args.add_match}")
        print(f"当前匹配关键字: {match_keywords}\n")
        exit()
    if args.del_match:
        match_keywords = delete_match_keywords(args.del_match)
        print(f"删除匹配关键字: {args.del_match}")
        print(f"当前匹配关键字: {match_keywords}\n")
        exit()
        
    if not args.path:
        #parser.print_help()
        return

    # 如果通过命令行指定了模式，使用命令行指定的模式
    if args.pattern:
        patterns = args.pattern
        print("匹配词: "+ str(patterns)+"\n")
    # 如果通过命令行指定了匹配关键字，使用命令行指定的关键字
 
    if args.match:
        start_time = time.time()
        print(f"匹配关键字: {match_keywords}\n")
        flag_regex = '|'.join(map(re.escape, match_keywords))
        for file_path in get_all_files(search_path):
            matches = search_flag_in_file(file_path, flag_regex)
            for line_num, line_content, flag_format in matches:
                result = f'文件名: {file_path}\n行号: {line_num}\n内容: {line_content}\n匹配的flag格式: {flag_format}\n'
                print(result)
                if output_file:
                    with open(output_file, "a") as out:
                        out.write(result + '\n')
        end_time = time.time()
        print(f'搜索完成，用时：{end_time - start_time}秒')
        exit()
    
    if patterns:
        print(f"匹配词: {patterns}\n")
    else:
        print("警告：没有指定匹配词。请使用 --add 添加匹配词或使用 -p 指定匹配词。")
        
    start_time = time.time()    
    for file_path in get_all_files(search_path):    
        for pattern in patterns:
            for encoder in CLASSES:
                try:
                    encoder.set_text(pattern)
                    regex = encoder.re
                    encoder_name = encoder.name
                    encode_text = encoder.encode_text
                    matches = search_flag_in_file(file_path, regex)
                    for line_num, line_content, math_result in matches:
                        if math_result:
                            decode_text = encoder.decode(math_result)
                            result = f'文件名: {file_path}\n行号: {line_num}\n匹配行: {line_content}\n匹配结果: {math_result}\n尝试解码: {decode_text}\n匹配格式: {encode_text}\n编码器: {encoder_name}\n'
                        else:
                            result = f'文件名: {file_path}\n行号: {line_num}\n匹配行: {line_content}\n匹配结果: {math_result}\n匹配格式: {encode_text}\n编码器: {encoder_name}\n'
                        print(result)
                        if output_file:
                            with open(output_file, "a") as out:
                                out.write(result + '\n')
                except NotImplementedError as e:
                    pass
                except Exception as e:
                    print(f"错误: {encoder.name} 发生异常: {str(e)}")
    end_time = time.time()
    print(f"以上结果基于匹配词: {patterns}, 添加更多匹配词请使用 --add 参数")
    print(f'搜索完成，用时：{end_time - start_time}秒')

if __name__ == "__main__":
    main()