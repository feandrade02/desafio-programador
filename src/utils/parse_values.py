import re

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
