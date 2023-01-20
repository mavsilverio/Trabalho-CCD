from PIL import Image

        """Compressor"""

        def get_size(i):
            width, height = i.size
            return width, height

        """Compress Function"""

        def compress(input_image, c_file):
            i_image = Image.open(input_image, 'r')
            c_list = []
            px = i_image.getdata()
            pp = None
            x = 0
            for p in px:
                if p == pp:
                    x += 1
                else:
                    if pp is not None:
                        pvalue = 0 if pp == 0 else 1
                        c_list.append((x, pvalue))
                    pp = p
                    x = 1
            with open(c_file, 'w+') as f:
                w = get_size(i_image)[0]
                h = get_size(i_image)[1]
                f.write('P1\n')
                f.write('#Compressão Manual\n')
                f.write('%s %s\n' % (w, h))
                for v in range(3):
                    for z, pvalue in c_list:
                        f.write(str(z))
                        f.write(str(','))
            return c_list

        def descomprimido(ficheiro):
            l1 = []
            l2 = []
            for v in range(3):
                with open(ficheiro, 'r') as f:
                    for x in f:
                        l1 = x.split(',')
                        l1.pop()
            for a in range(len(l1)):
                l1[a] = int(l1[a])
            i = 0
            for z in l1:
                for v in range(z):
                    l2.append(i)
                i = (i + 1) % 2

            with open(output_file, 'w+') as f2:
                with open(ficheiro, 'r') as f:
                    c = 0
                    for linhas in f:
                        if c == 1:
                            f2.write("#Descompressão Manual\n")
                        if c != 1 and c < 3:
                            f2.write(linhas)
                        c = c + 1

                c = 0
                for v2 in l2:
                    if c <= 70:
                        f2.write(str(v2))
                        c = c + 1
                    if c == 70:
                        f2.write('\n')
                        c = 0
            return

        # Open the image and compress it
        compress(eval(input("inserir nome do documento")), 'Compressed File.txt')
        descomprimido('Compressed File.txt')
