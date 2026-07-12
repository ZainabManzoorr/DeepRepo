class SymbolTable:
  
  def __init__(self):
     
       self.symbols = {}
  def add_symbol(
        self,
        name: str,
        file: str,
        symbol_type: str,
        line: int
  ):
    self.symbols[name] = {
        "file": file,
        "type": symbol_type,
        "line": line
    }
  def lookup(
        self,
        name: str
  ):
    return self.symbols.get(name)
  
  def exits(
        self,
        name: str
  ) -> bool:
    return name in self.symbols
  def all_symbols(self):
    return self.symbols
  def clear(self):
    self.symbols.clear()
    
  def __len__(self):
    return len(self.symbols)
  
  def resolve_function_file(self, function_name: str):
    """
    Return file where function is defined
    """
    symbol = self.symbols.get(function_name)
    if symbol:
        return symbol["file"]
    return None
  
print("\nSYMBOL TABLE")
