"""
地図生成インフラストラクチャ

foliumライブラリを使用した地図HTML生成の具象実装
"""

import folium
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
import tempfile
import os

from domain.models.photo import Photo, GPSCoordinates
from utils.exceptions import InfrastructureError


class MapGenerator:
    """
    地図生成クラス
    
    foliumを使用してGPS情報付き写真の地図を生成
    """
    
    def __init__(self, default_zoom: int = 15):
        """
        初期化
        
        Args:
            default_zoom: デフォルトのズームレベル
        """
        self.default_zoom = default_zoom
        self._temp_files = []  # 生成した一時ファイルの管理
    
    def generate_single_photo_map(
        self, 
        photo: Photo, 
        output_path: Optional[Path] = None
    ) -> Path:
        """
        単一写真の地図を生成
        
        Args:
            photo: GPS情報を持つ写真
            output_path: 出力ファイルパス（Noneの場合は一時ファイル）
            
        Returns:
            Path: 生成された地図ファイルのパス
            
        Raises:
            InfrastructureError: GPS情報がない、または生成に失敗した場合
        """
        if not photo.has_gps_data:
            raise InfrastructureError(f"写真にGPS情報がありません: {photo.file_name}")
        
        try:
            # 地図を作成
            lat, lon = photo.gps_coordinates.to_tuple()
            map_obj = folium.Map(location=[lat, lon], zoom_start=self.default_zoom)
            
            # マーカーを追加
            popup_text = self._create_popup_text(photo)
            folium.Marker(
                [lat, lon],
                popup=popup_text,
                tooltip=photo.file_name
            ).add_to(map_obj)
            
            # ファイルに保存
            if output_path is None:
                output_path = self._create_temp_file("single_photo_map.html")
            
            map_obj.save(str(output_path))
            return output_path
            
        except Exception as e:
            raise InfrastructureError(f"地図生成エラー: {e}") from e
    
    def generate_multi_photo_map(
        self, 
        photos: List[Photo], 
        output_path: Optional[Path] = None,
        cluster_markers: bool = True
    ) -> Path:
        """
        複数写真の地図を生成
        
        Args:
            photos: GPS情報を持つ写真のリスト
            output_path: 出力ファイルパス（Noneの場合は一時ファイル）
            cluster_markers: マーカーをクラスター化するか
            
        Returns:
            Path: 生成された地図ファイルのパス
            
        Raises:
            InfrastructureError: GPS情報を持つ写真がない、または生成に失敗した場合
        """
        # GPS情報を持つ写真のみをフィルタ
        gps_photos = [photo for photo in photos if photo.has_gps_data]
        
        if not gps_photos:
            raise InfrastructureError("GPS情報を持つ写真がありません")
        
        try:
            # 地図の中心とズームレベルを計算
            center_lat, center_lon, zoom_level = self._calculate_map_bounds(gps_photos)
            
            # 地図を作成
            map_obj = folium.Map(
                location=[center_lat, center_lon], 
                zoom_start=zoom_level
            )
            
            # クラスター化の設定
            if cluster_markers and len(gps_photos) > 1:
                from folium.plugins import MarkerCluster
                marker_cluster = MarkerCluster().add_to(map_obj)
                marker_container = marker_cluster
            else:
                marker_container = map_obj
            
            # 各写真のマーカーを追加
            for photo in gps_photos:
                lat, lon = photo.gps_coordinates.to_tuple()
                popup_text = self._create_popup_text(photo)
                
                folium.Marker(
                    [lat, lon],
                    popup=popup_text,
                    tooltip=photo.file_name
                ).add_to(marker_container)
            
            # パスラインを追加（撮影時刻順）
            if len(gps_photos) > 1:
                self._add_path_line(map_obj, gps_photos)
            
            # ファイルに保存
            if output_path is None:
                output_path = self._create_temp_file("multi_photo_map.html")
            
            map_obj.save(str(output_path))
            return output_path
            
        except Exception as e:
            raise InfrastructureError(f"地図生成エラー: {e}") from e
    
    def generate_journey_map(
        self, 
        photos: List[Photo], 
        output_path: Optional[Path] = None
    ) -> Path:
        """
        旅行ルート地図を生成
        
        撮影時刻順に写真を並べて、移動ルートを可視化
        
        Args:
            photos: 写真のリスト
            output_path: 出力ファイルパス
            
        Returns:
            Path: 生成された地図ファイルのパス
        """
        # GPS情報と撮影時刻を持つ写真のみをフィルタ・ソート
        valid_photos = [
            photo for photo in photos 
            if photo.has_gps_data and photo.taken_date
        ]
        valid_photos.sort(key=lambda p: p.taken_date)
        
        if len(valid_photos) < 2:
            raise InfrastructureError("旅行ルートを作成するには、GPS情報と撮影時刻を持つ写真が2枚以上必要です")
        
        try:
            # 地図の設定
            center_lat, center_lon, zoom_level = self._calculate_map_bounds(valid_photos)
            map_obj = folium.Map(
                location=[center_lat, center_lon], 
                zoom_start=zoom_level
            )
            
            # 開始・終了マーカーを追加
            start_photo = valid_photos[0]
            end_photo = valid_photos[-1]
            
            start_lat, start_lon = start_photo.gps_coordinates.to_tuple()
            end_lat, end_lon = end_photo.gps_coordinates.to_tuple()
            
            # 開始地点マーカー
            folium.Marker(
                [start_lat, start_lon],
                popup=f"開始: {self._create_popup_text(start_photo)}",
                tooltip="旅行開始",
                icon=folium.Icon(color='green', icon='play')
            ).add_to(map_obj)
            
            # 終了地点マーカー
            folium.Marker(
                [end_lat, end_lon],
                popup=f"終了: {self._create_popup_text(end_photo)}",
                tooltip="旅行終了",
                icon=folium.Icon(color='red', icon='stop')
            ).add_to(map_obj)
            
            # 中間地点のマーカー
            for i, photo in enumerate(valid_photos[1:-1], 1):
                lat, lon = photo.gps_coordinates.to_tuple()
                folium.CircleMarker(
                    [lat, lon],
                    radius=5,
                    popup=self._create_popup_text(photo),
                    tooltip=f"地点 {i}",
                    color='blue',
                    fill=True
                ).add_to(map_obj)
            
            # ルートライン
            self._add_journey_line(map_obj, valid_photos)
            
            # ファイルに保存
            if output_path is None:
                output_path = self._create_temp_file("journey_map.html")
            
            map_obj.save(str(output_path))
            return output_path
            
        except Exception as e:
            raise InfrastructureError(f"旅行ルート地図生成エラー: {e}") from e
    
    def cleanup_temp_files(self) -> None:
        """生成した一時ファイルをクリーンアップ"""
        for temp_file in self._temp_files:
            try:
                if temp_file.exists():
                    temp_file.unlink()
            except Exception:
                pass
        self._temp_files.clear()
    
    def _create_popup_text(self, photo: Photo) -> str:
        """
        ポップアップテキストを作成
        
        Args:
            photo: 写真オブジェクト
            
        Returns:
            str: ポップアップ用のHTMLテキスト
        """
        html_parts = [f"<b>{photo.file_name}</b><br>"]
        
        if photo.taken_date:
            date_str = photo.taken_date.strftime("%Y年%m月%d日 %H:%M:%S")
            html_parts.append(f"撮影日時: {date_str}<br>")
        
        if photo.metadata:
            if photo.metadata.camera_make and photo.metadata.camera_model:
                html_parts.append(f"カメラ: {photo.metadata.camera_make} {photo.metadata.camera_model}<br>")
            
            if photo.metadata.width and photo.metadata.height:
                html_parts.append(f"解像度: {photo.metadata.width} × {photo.metadata.height}<br>")
        
        if photo.gps_coordinates:
            lat, lon = photo.gps_coordinates.to_tuple()
            html_parts.append(f"座標: {lat:.6f}, {lon:.6f}")
        
        return "".join(html_parts)
    
    def _calculate_map_bounds(self, photos: List[Photo]) -> Tuple[float, float, int]:
        """
        地図の中心点とズームレベルを計算
        
        Args:
            photos: GPS情報を持つ写真のリスト
            
        Returns:
            Tuple[float, float, int]: (中心緯度, 中心経度, ズームレベル)
        """
        if not photos:
            return (35.6762, 139.6503, self.default_zoom)  # 東京駅
        
        if len(photos) == 1:
            lat, lon = photos[0].gps_coordinates.to_tuple()
            return (lat, lon, self.default_zoom)
        
        # 境界を計算
        latitudes = [float(photo.gps_coordinates.latitude) for photo in photos]
        longitudes = [float(photo.gps_coordinates.longitude) for photo in photos]
        
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)
        
        # 中心点
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2
        
        # ズームレベルを距離に基づいて計算
        lat_diff = max_lat - min_lat
        lon_diff = max_lon - min_lon
        max_diff = max(lat_diff, lon_diff)
        
        if max_diff < 0.001:
            zoom_level = 17
        elif max_diff < 0.01:
            zoom_level = 14
        elif max_diff < 0.1:
            zoom_level = 11
        elif max_diff < 1.0:
            zoom_level = 8
        else:
            zoom_level = 5
        
        return (center_lat, center_lon, zoom_level)
    
    def _add_path_line(self, map_obj, photos: List[Photo]) -> None:
        """
        パスラインを地図に追加
        
        Args:
            map_obj: Foliumマップオブジェクト
            photos: 写真リスト
        """
        if len(photos) < 2:
            return
        
        # 撮影時刻でソート
        sorted_photos = sorted(
            [p for p in photos if p.taken_date], 
            key=lambda p: p.taken_date
        )
        
        if len(sorted_photos) < 2:
            return
        
        # 座標リストを作成
        coordinates = [photo.gps_coordinates.to_tuple() for photo in sorted_photos]
        
        # パスラインを追加
        folium.PolyLine(
            coordinates,
            color='red',
            weight=2,
            opacity=0.7,
            popup="撮影ルート"
        ).add_to(map_obj)
    
    def _add_journey_line(self, map_obj, photos: List[Photo]) -> None:
        """
        旅行ルートラインを地図に追加
        
        Args:
            map_obj: Foliumマップオブジェクト
            photos: 時系列順の写真リスト
        """
        if len(photos) < 2:
            return
        
        coordinates = [photo.gps_coordinates.to_tuple() for photo in photos]
        
        # メインの旅行ルート
        folium.PolyLine(
            coordinates,
            color='blue',
            weight=3,
            opacity=0.8,
            popup="旅行ルート"
        ).add_to(map_obj)
        
        # 方向矢印（簡単な実装）
        for i in range(len(coordinates) - 1):
            mid_lat = (coordinates[i][0] + coordinates[i+1][0]) / 2
            mid_lon = (coordinates[i][1] + coordinates[i+1][1]) / 2
            
            folium.CircleMarker(
                [mid_lat, mid_lon],
                radius=3,
                color='darkblue',
                fill=True,
                popup=f"区間 {i+1}"
            ).add_to(map_obj)
    
    def _create_temp_file(self, suffix: str) -> Path:
        """
        一時ファイルを作成
        
        Args:
            suffix: ファイル名のサフィックス
            
        Returns:
            Path: 一時ファイルのパス
        """
        temp_dir = Path(tempfile.gettempdir())
        temp_file = temp_dir / f"photomap_{suffix}"
        self._temp_files.append(temp_file)
        return temp_file
