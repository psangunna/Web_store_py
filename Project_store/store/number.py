

"""La función toma como entrada un tipo de referencia (reftype), 
 una clase de modelo (model_class) y un indicador opcional (add_filter).
 Genera un número de referencia único basado en el tipo de referencia y 
 la información existente en los objetos de la clase de modelo. 
 Creación de números de referencia para: suppliers, invoices, orders, categories
"""
def create_ref_number(reftype, model_class,add_filter = False  ):
   
    ref_number = None
    if add_filter == False:
        object_master_obj = model_class.objects.first()
    else:
        object_master_obj = model_class.objects.filter(saved_later=False).order_by('-created').first()


    if object_master_obj:
        ref_number = object_master_obj.ref_no
  
        if ref_number:
            
            var = ref_number.split(reftype + '-')
            var = int(var[-1]) + 1
            var = str(var)
            last_no = var.zfill(10)
            ref_number = reftype + "-" + last_no
            return ref_number
    else:
    
        last_no = "1"
        ref_number = reftype + '-' + last_no.zfill(10)
   

    return ref_number