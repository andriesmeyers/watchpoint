<?php

class StringHelper {
	
	public static function decodeString($string){
		return str_replace('\'', '',  
					str_replace(',', '', 
						str_replace('&', 'en', 
							str_replace(' ','', 
								strtolower($string)))));
	}
}
?>