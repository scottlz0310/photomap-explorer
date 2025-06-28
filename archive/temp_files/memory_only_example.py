def generate_map_html_memory_only(lat, lon):
    """メモリ内のみでマップHTMLを生成（一時ファイルなし）"""
    import io
    
    # Foliumマップを作成
    map_obj = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], tooltip="画像の位置").add_to(map_obj)
    
    # StringIOを使用してメモリ内でHTMLを生成
    output = io.StringIO()
    map_obj.save(output, close_file=False)
    html_content = output.getvalue()
    output.close()
    
    return html_content
