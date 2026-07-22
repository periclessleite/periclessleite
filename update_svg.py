import os
import re

source_svg_path = "profile-3d-contrib/night.svg"
output_path = "git-stats/night-stats.svg"

if os.path.exists(source_svg_path):
    with open(source_svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    # 1. Reduz a altura total do viewBox e da tag <svg> para 500 (removendo as margens verticais)
    svg_content = re.sub(r'height="850"', 'height="500"', svg_content)
    svg_content = re.sub(r'viewBox="0 0 1280 850"', 'viewBox="0 0 1280 500"', svg_content)

    # 2. Altera o fundo para garantir o tom escuro correto
    svg_content = re.sub(r'<rect x="0" y="0" width="1280" height="850" fill="[^"]+"></rect>', 
                         '<rect x="0" y="0" width="1280" height="500" fill="#00000f"></rect>', svg_content)

    # 3. Remove completamente a barra central isométrica (o bloco de blocos coloridos de contribuição diária)
    # Procuramos e removemos a grande faixa de tags <g transform="translate(...)"> que desenham os cubos
    svg_content = re.sub(r'<g>\s*<g transform="translate\(140 154\.18\)".*?</svg>', '</svg>', svg_content, flags=re.DOTALL)

    # 4. Centraliza o Gráfico de Radar na vertical (movendo de Y=284.5 para Y=250)
    svg_content = svg_content.replace('transform="translate(980, 284.5)"', 'transform="translate(980, 250)"')

    # 5. Centraliza o Gráfico de Pizza/Linguagens na vertical (movendo de Y=520 para Y=120)
    svg_content = svg_content.replace('transform="translate(40, 520)"', 'transform="translate(120, 120)"')
    svg_content = svg_content.replace('transform="translate(130, 130)"', 'transform="translate(130, 130)"') # Mantém o miolo

    # 6. Reposiciona o bloco de rodapé (contribuições, stars, PRs) para o centro inferior e mais para cima (Y=468)
    # Localiza o grupo do rodapé contendo "contributions" e ajusta suas coordenadas Y de 830 para 468
    svg_content = re.sub(r' y="830"', ' y="468"', svg_content)
    
    # Ajusta os ícones do rodapé que estavam em Y=802 para Y=440
    svg_content = re.sub(r'transform="translate\((\d+),\s*802\),\s*scale\(2\)"', r'transform="translate(\1, 440) scale(2)"', svg_content)

    os.makedirs("git-stats", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Sucesso absoluto: SVG limpo, com pizza, radar e dados reais gerados!")
else:
    print("Erro: O arquivo original da action não foi encontrado.")