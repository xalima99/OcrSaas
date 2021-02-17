from app.scripts.helpers import (is_alpha_numeric, is_date, is_id, is_uppercase, has_alpha,
 has_numeric, extract_genre, extract_parents_name, extract_place)

class TestClass:
    def test_is_alpha_numeric(self):
        assert is_alpha_numeric('iamanalphanumericwrittenin2020') == True
        assert is_alpha_numeric('778888888') == True
        assert is_alpha_numeric('*') == False
    
    def test_is_date(self):
        assert is_date("12.13.2002") == True
        assert is_date("122.13.2002") == False
        assert is_date("12213.2002") == False
        assert is_date("12.2132002") == True
        
    def test_id_id(self):
        assert is_id("WP002966") == True
        assert is_id("02966") == False
        assert is_id("WP*02966") == False
        
    def test_is_uppercase(self):
        assert is_uppercase("OCRASASAAS") == True
        assert is_uppercase("OCRASASAAs") == False
        assert is_uppercase("OcRAcAScAS") == False
        
    def test_has_alpha(self):
        assert has_alpha("OCRASASAAS") == True
        assert has_alpha("123456789") == False
        assert has_alpha("1r2r34r4r") == True
        
    def test_has_numeric(self):
        assert has_numeric("OCRASASAAS") == False
        assert has_numeric("123456789") == True
        assert has_numeric("1r2r34r4r") == True
        
    def test_extract_genre(self):
        assert extract_genre("sexe M hello") == 'M'
        assert extract_genre("sexe F hello") == 'F'
        
    def test_extract_parents_name(self):
        assert extract_parents_name("fils de KARIM DIALLO") == 'KARIM DIALLO'
        assert extract_parents_name("et de AMINATA DIOP FALL SECK") == 'AMINATA DIOP FALL SECK'
        
    def test_extract_place(self):
        assert extract_place("à Casablanca") == 'Casablanca'
        assert extract_place("Nationalité Casablanca") == 'Casablanca'
        assert extract_place("Nationalité SENEGALAISE") == 'SENEGALAISE'
        assert extract_place("à SENEGALAISE") == 'SENEGALAISE'
        
        