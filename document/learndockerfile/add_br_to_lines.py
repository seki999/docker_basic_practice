def add_br_to_lines(input_filename, output_filename):
    # 读取输入文件所有行
    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # 写入处理后的内容到输出文件
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in lines:
            # 去除所有 '*'、'---' 和 '#' 符号
            line = line.replace('*', '').replace('---', '').replace('#', '')
            
            # 去除行尾换行符，但保留其他空白字符
            line_content = line.rstrip('\n')
            
            # 如果该行（去除首尾空白后）为空，则跳过该行
            if line_content.strip() == '':
                continue
            
            # 如果该行末尾已经包含 <br>（忽略行尾可能的空白字符），则不做处理
            if line_content.rstrip().endswith('<br>'):
                outfile.write(line_content + '\n')
            else:
                outfile.write(line_content + '<br>\n')

if __name__ == '__main__':
    input_file = 'manifest创建多架构镜像.html'    # 输入 HTML 文件路径
    output_file = 'manifest创建多架构镜像2.html'  # 输出 HTML 文件路径
    add_br_to_lines(input_file, output_file)
