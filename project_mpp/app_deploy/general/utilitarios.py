def getMonthName(month):
    
    if type(month) == str:
        month = int(month)

    month_name = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio','Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    return month_name[month-1]
