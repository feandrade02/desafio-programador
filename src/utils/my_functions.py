import re
from PIL import Image

def parse_value(text) -> float | None:
        """
        Limpa e converte uma string de moeda (ex: "1.115,31") 
        para um valor numérico float (ex: 1115.31).
        """
        if text is None or text.strip() == "":
            return None
        
        # Remove pontos (milhares) e substitui vírgula (decimal) por ponto
        clean_value = text.strip().replace(".", "").replace(",", ".")
        
        # Remove quaisquer caracteres não numéricos restantes (exceto o ponto decimal)
        clean_value = re.sub(r"[^0-9\.]", "", clean_value)
        
        try:
            return float(clean_value)
        except ValueError:
            return None

def binarize_image(image: Image.Image, threshold: int = 180) -> Image.Image:
    """Converte uma imagem do Pillow para preto e branco puro com base em um limiar."""
    
    # Converte para escala de cinza
    grayscale_image = image.convert('L')
    
    # Aplica a binarização (thresholding)
    # O modo '1' cria uma imagem de 1-bit, preto e branco.
    binary_image = grayscale_image.point(lambda pixel: 0 if pixel < threshold else 255, '1')
    return binary_image