# coding=utf-8
import re

from app.scripts.helpers import (is_uppercase, is_date, is_id, extract_genre, extract_place,
extract_parents_name, has_alpha, has_numeric)

#test infos
infosEtr = ['ROYAUME DU MAROC', "CARTE NATIONLE D'IDENTITE", '4-191', 'YOUSSEF', '255', 'MOUGJA', 'Né le', '20.02 1986', 'autoblas', 'à AIT OURIBEL KHEMISSET', "Valable jusqu'au", '28.10.2022', 'ale arlo', 'whgll coll plell wrall', 'AB631198', 'MW', 'following', 'N°', 'AB631198', 'p)', "Valable jusqu'au 28.10.2022 alc Walle", 'gis ir - cate', '40 LC is able 9', 'Fils de', 'LAHCEN ben HADDOU', 'et de FATIMA bent ABDELLAH', '24 in as; obgell', 'Adresse RUE MANGOUB NO 24 HAY FARAH KARIA SALE', 'N° état civil', '102/1986', 'wiall allow pl', 'Sexe', 'M']
infosNat = [ 'ROYAUME DU MAROC',
"DARTE D'IMMATRICULATION",
'hamillable',
'seel',
'AMADOU',
'Jla',
'FALL',
'Na le',
'27.11.1905',
'Buly alee',
'hameall',
'Nationalité SENEGALAISE',
'Valable du',
'06.10.2017',
'au',
'29.06.2020',
'wl',
'whell plall small',
'W002966P',
'MH',
'Qay,',
'jion Jall 46',
'N°',
'W002966P ab',
 'Sexe M Mall',
'11b aolyvi',
'Motif de séjour ETUDES',
'ulgiell',
'Adresse LOTISSEMENT AL AMAL RUE 05 NR11 SETTAT',
'will chail algo> N plel (10) duice Jal Bls di zua of dio me']


class IdCard:
    #indexes
    is_card_valid = None
    error_card = ""
    index_of_Imma = None
    index_of_name = None
    index_of_birth_date = None
    index_of_creation_date = None
    index_of_expiry_date = None
    index_of_birth_place = None
    index_of_word_civil = None
    index_of_civil_number = None
    index_of_pere = None
    index_of_mere = None
    #CHECKS - To confirm that all needed infos
    #are successfully extracted
    check_names = False
    check_birth_date = False
    check_creation_date = False
    check_expiry_date = False
    check_birth_place = False
    check_number_cin = False
    check_address = False
    check_civil_number = False
    check_name_father = False
    check_name_mother = False
    check_genre = False
    check_type_card = False
    
    
    
    @staticmethod
    def findWholeWord(w: str):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    def __init__(self, id_card: dict):
        self.card = id_card
        self.result = {
            "type_card": "",
            "first_name": "",
            "last_name": "",
            "birth_date": "",
            # "creation_date": "",
            "expiry_date": "",
            "birth_place": "",
            "number_cin": "",
            "address": "",
            # "civil_number": "",
            # "name_father": "",
            # "name_mother": "",
            "genre": ""
         }
    
    def get_names(self):
        first_name_found = False
        last_name_found = False

        for index, value in enumerate(self.card):
            #find type of id card
            if not IdCard.is_card_valid:
                if "MATRICULATION" in value or bool(
                IdCard.findWholeWord("IDENTITE")(value)):
                    IdCard.is_card_valid = True
                    IdCard.index_of_Imma = index
                    if "MATRICULATION" in value:
                        self.result['type_card'] = "Sejour"
                    else:
                        self.result['type_card'] = "Nationale"
                    IdCard.check_type_card = True
            
            #Name extracting logic after type card found
            if IdCard.index_of_Imma:
                #finding first name
                if (index > IdCard.index_of_Imma and not first_name_found and 
                is_uppercase(value) and has_alpha(value) and not has_numeric(value)
                and len(value) > 1):
                    IdCard.index_of_name = index
                    self.result['first_name'] = value
                    first_name_found = True
                #finding last name
                if (first_name_found and index > IdCard.index_of_name and 
                    index - IdCard.index_of_name < 4 and not last_name_found and is_uppercase(value) and
                    has_alpha(value) and len(value) and not has_numeric(value)):
                        self.result['last_name'] = value
                        last_name_found = True
        
        if first_name_found and last_name_found:
            IdCard.check_names = True
        else:
            #Error while checking name or usernames
            IdCard.is_card_valid = False
            IdCard.error_card = "Error finding Names"
    
    def get_dates(self):
        birth_date_found = False
        creation_date_found = False
        expiry_date_found = False
        
        for index, value in enumerate(self.card):
            #find birthdate
            if not birth_date_found and is_date(value):
                IdCard.index_of_birth_date = index
                self.result['birth_date'] = value
                birth_date_found = True
                IdCard.check_birth_date = True
            
            if (self.result['type_card'] == "Sejour" and birth_date_found and
                index > IdCard.index_of_birth_date and not creation_date_found and
                is_date(value)):
                #find creation date (only available on sejour cards)
                IdCard.index_of_creation_date = index
                self.result['creation_date'] = value
                creation_date_found = True
                IdCard.check_creation_date = True
            
            if (self.result['type_card'] == "Sejour" and creation_date_found and 
                index > IdCard.index_of_creation_date and not expiry_date_found and
                    is_date(value)):
                IdCard.index_of_expiry_date = index
                self.result['expiry_date'] = value
                expiry_date_found = True
                IdCard.check_expiry_date = True
            
            if (self.result['type_card'] == "Nationale" and birth_date_found and
                index > IdCard.index_of_birth_date and not expiry_date_found and
                is_date(value)):
                IdCard.index_of_expiry_date = index
                self.result['expiry_date'] = value
                expiry_date_found = True
                IdCard.check_expiry_date = True
                
        if birth_date_found and expiry_date_found:
            pass
        else:
            #Error while checking name or usernames
            IdCard.is_card_valid = False
            IdCard.error_card = "Error finding dates"
    
    def get_birth_place(self):
        birth_place_found = False
        
        for index, value in enumerate(self.card):
            if "Nationa" in value and not birth_place_found and index > IdCard.index_of_birth_date:
                IdCard.index_of_birth_place = index
                birth_place_found = True
                self.result['birth_place'] = value
                IdCard.check_birth_place = True
                
            if value[0] == 'à' and not birth_place_found:
                clean_place_name = extract_place(value)
                if is_uppercase(clean_place_name):
                    IdCard.index_of_birth_place = index
                    birth_place_found = True
                    self.result['birth_place'] = clean_place_name
                    IdCard.check_birth_place = True
        
        if birth_place_found:
            pass
        else:
            #Error while checking name or usernames
            IdCard.is_card_valid = False
            IdCard.error_card = "Error finding birth place"
    
    def get_id(self):
        id_number_found = False
        
        for value in self.card:
            if (is_uppercase(value) and is_id(value) and not id_number_found):
                id_number_found = True
                self.result['number_cin'] = value
                IdCard.check_number_cin = True
        
        if id_number_found:
            pass
        else:
            #Error while checking name or usernames
            IdCard.is_card_valid = False
            IdCard.error_card = "Error finding CIN number"
    
    def get_address(self):
        address_found = False
        
        for value in self.card:
            if 'dresse' in value and not address_found:
                clean_address = extract_place(value)
                if is_uppercase(clean_address):
                    self.result['address'] = clean_address
                    IdCard.check_address = True
                    address_found = True
        
        if address_found:
            pass
        else:
            #Error while checking name or usernames
            IdCard.is_card_valid = False
            IdCard.error_card = "Error finding Adresse"
    
    def get_civil_number(self):
        civil_word_found = False
        civil_number_found = False
        
        if self.result['type_card'] == "Nationale":
            for index, value in enumerate(self.card):
                if 'civil' in value and not civil_word_found:
                    civil_word_found = True
                    IdCard.index_of_word_civil = index
                
                if (civil_word_found and not civil_number_found and
                    index > IdCard.index_of_word_civil and is_uppercase(value)
                    and len(value) >= 4):
                    civil_number_found = True
                    IdCard.index_of_civil_number = index
                    self.result['civil_number'] = value
                    IdCard.check_civil_number = True
                    
    def get_parents_names(self):
        fils_word_found = False
        fils_word_index = None
        pere_name_found = False
        mere_name_found = False
        
        if self.result['type_card'] == "Nationale":
            for index, value in enumerate(self.card):
                if 'ils de' in value and not pere_name_found:
                    fils_word_found = True
                    fils_word_index = index
                    if len(value.split()) >= 4:
                        self.result['name_father'] = extract_parents_name(value)
                        IdCard.check_name_father = True
                        pere_name_found = True
                        IdCard.index_of_pere = index
                
                if fils_word_found and not pere_name_found and index - fils_word_index == 1:
                    self.result['name_father'] = value
                    IdCard.check_name_father = True
                    pere_name_found = True
                    IdCard.index_of_pere = index
                    
                if ('et de' in value and pere_name_found and not mere_name_found 
                    and index > IdCard.index_of_pere):
                    self.result['name_mother'] = extract_parents_name(value)
                    IdCard.check_name_mother = True
                    mere_name_found = True
                    IdCard.index_of_mere = index
    
    def get_genre(self):
        sex_word_found = False
        index_of_sex_word = None
        genre_found = False
        
        for index, value in enumerate(self.card):
            if 'Sex' in value:
                sex_word_found = True
                index_of_sex_word = True
                if len(value.split()) >= 2:
                    self.result['genre'] = extract_genre(value)
                    IdCard.check_genre = True
            
            if (sex_word_found and index > index_of_sex_word and not genre_found and is_uppercase(value)
                and len(value) == 1):
                self.result['genre'] = value
                IdCard.check_genre = True
        
        if sex_word_found and genre_found:
            pass
        else:
            #Error while checking name or usernames
            IdCard.is_card_valid = False
            IdCard.error_card = "Error finding genre"
                
    def scan(self):
        self.get_names()
        if not IdCard.is_card_valid:
            return {
                "message": "Error reading card",
                "error": IdCard.error_card
            }
        self.get_dates()
        self.get_birth_place()
        self.get_id()
        self.get_address()
        if self.result['type_card'] == "Nationale":
            self.get_civil_number()
            self.get_parents_names()
        self.get_genre()
        
        if self.result['type_card'] == "Nationale":
            national_check = IdCard.check_name_father and IdCard.check_name_mother and IdCard.check_civil_number
        elif self.result['type_card'] == "Sejour":
            sejour_check = IdCard.check_creation_date
        
        general_check = (IdCard.check_names and IdCard.check_birth_date and IdCard.check_birth_place 
                         and IdCard.check_expiry_date and IdCard.check_genre and IdCard.check_number_cin)
        
        if self.result['type_card'] == "Nationale":
            
            if general_check and national_check:
                return self.result
            else:
                return {
                    "message": "Error reading card",
                    "error": IdCard.error_card
                }
            
        if self.result['type_card'] == "Sejour":
            if general_check and sejour_check:
                return self.result
            else:
                return {
                    "message": "Error reading card",
                    "error": IdCard.error_card
                }
