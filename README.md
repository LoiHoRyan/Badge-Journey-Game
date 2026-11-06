# 🏅 HÀNH TRÌNH HUY HIỆU (BADGE JOURNEY)

> **Chơi để khám phá – Học để vươn xa.**

**Hành Trình Huy Hiệu (Badge Journey)** là một tựa game platformer 2D mang phong cách pixel-art kết hợp hoạt hình, được xây dựng bằng Python. Người chơi đồng hành cùng nhân vật hiệp sĩ, khám phá những vùng đất khác nhau, vượt qua thử thách, thu thập huy hiệu và tiến đến những cột mốc mới trong hành trình.

Dự án hướng đến trải nghiệm giải trí kết hợp khám phá và học hỏi, với thế giới game có màu sắc tươi sáng, phù hợp với trẻ em và thanh thiếu niên.

---

## ✨ Điểm nổi bật

- **Thế giới đa dạng:** hành trình được thiết kế qua nhiều vùng đất với bối cảnh và thử thách riêng.
- **Khám phá và thu thập:** người chơi di chuyển qua các màn chơi, thu thập huy hiệu và mở rộng hành trình.
- **Thử thách và chiến đấu:** đối mặt với chướng ngại vật, kẻ địch và trùm cuối.
- **Hệ thống kỹ năng:** sử dụng các kỹ năng theo phím Q, E, R và T; mỗi kỹ năng tiêu hao một lượng mana khác nhau.
- **Phong cách hình ảnh:** đồ họa pixel-art tươi sáng, kết hợp cảm giác phiêu lưu kỳ ảo.
- **Dữ liệu màn chơi:** các thông tin màn chơi được tổ chức bằng dữ liệu để thuận tiện quản lý và phát triển.

## 🌍 Thế giới trong game

Hành trình dự kiến đi qua 10 thế giới:

| STT | Thế giới |
|---:|---|
| 1 | Đồng cỏ |
| 2 | Sa mạc |
| 3 | Bãi biển |
| 4 | Rừng sâu |
| 5 | Vùng tuyết |
| 6 | Núi lửa |
| 7 | Thành phố trên mây |
| 8 | Nhà máy cơ khí |
| 9 | Không gian |
| 10 | Đền cổ cuối cùng |

*Danh sách trên thể hiện định hướng thiết kế của dự án; nội dung và tiến độ từng thế giới có thể thay đổi trong quá trình phát triển.*

## 🕹️ Điều khiển

| Phím | Chức năng |
|---|---|
| Q | Sử dụng kỹ năng Q (tiêu hao 20 mana) |
| E | Sử dụng kỹ năng E (tiêu hao 30 mana) |
| R | Sử dụng kỹ năng R (tiêu hao 25 mana) |
| T | Sử dụng kỹ năng T (tiêu hao 60 mana) |

> Các phím di chuyển, nhảy, tương tác và những thao tác khác cần xem phần hướng dẫn trong game hoặc cấu hình điều khiển của phiên bản hiện tại.

## 🧰 Công nghệ và công cụ

- **Python:** ngôn ngữ lập trình chính.
- **JSON:** lưu trữ dữ liệu màn chơi.
- **Tiled:** công cụ thiết kế bản đồ (nếu được sử dụng trong phiên bản hiện tại).
- **PyInstaller:** cấu hình đóng gói ứng dụng desktop thông qua tệp `.spec`.

Các thư viện Python cần thiết được khai báo trong `requirements.txt`.

## 📁 Cấu trúc dự án

```text
Badge-Journey-Game/
├── assets/                 # Hình ảnh và tài nguyên game
├── data/                   # Dữ liệu phục vụ trò chơi
├── music/                  # Nhạc và âm thanh
├── saves/                  # Dữ liệu lưu trò chơi (nếu có)
├── main.py                 # Điểm khởi chạy chương trình
├── settings.py             # Các thiết lập của game
├── levels.json             # Dữ liệu màn chơi
├── game_icon.ico           # Biểu tượng game
├── requirements.txt        # Danh sách thư viện Python
├── Badge Journey.spec      # Cấu hình đóng gói PyInstaller
├── Badge Journey.md        # Tài liệu dự án
├── .gitignore              # Các tệp/thư mục không đưa lên Git
└── README.md               # Giới thiệu và hướng dẫn dự án
```

*Cấu trúc có thể được điều chỉnh theo phiên bản mã nguồn mới nhất.*

## 🚀 Cài đặt và chạy game

### 1. Yêu cầu

- Máy tính Windows, macOS hoặc Linux có cài Python tương thích với các thư viện trong dự án.
- Git (nếu tải mã nguồn bằng Git).
- Các tài nguyên đi kèm repository.

### 2. Tải mã nguồn

```bash
git clone https://github.com/LoiHoRyan/Badge-Journey-Game.git
cd Badge-Journey-Game
```

Hoặc tải repository dưới dạng ZIP từ GitHub và giải nén.

### 3. Tạo môi trường ảo (khuyến nghị)

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo:

**Windows (CMD):**
```bat
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 4. Cài đặt thư viện

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Khởi chạy

```bash
python main.py
```

Nếu dự án yêu cầu cấu hình hoặc tài nguyên bổ sung, hãy kiểm tra các hướng dẫn tương ứng trong thư mục và tài liệu đi kèm.

## 💾 Dữ liệu lưu trò chơi

Thư mục `saves/` được dành cho dữ liệu lưu tiến trình chơi nếu phiên bản hiện tại sử dụng cơ chế lưu này. Không nên đưa dữ liệu cá nhân hoặc tệp lưu riêng của người chơi lên repository công khai. Có thể cung cấp một tệp lưu mẫu riêng nếu cần thiết.

## 🛠️ Phát triển dự án

Bạn có thể đóng góp bằng cách:

1. Fork repository.
2. Tạo nhánh mới cho thay đổi của mình.
3. Thực hiện và kiểm tra thay đổi.
4. Gửi Pull Request kèm mô tả rõ ràng.

Khi bổ sung tài nguyên, hãy đặt chúng vào đúng thư mục và cập nhật đường dẫn tham chiếu trong mã nguồn hoặc dữ liệu game.

## 📌 Trạng thái dự án

Badge Journey đang trong quá trình phát triển. Tính năng, màn chơi, hình ảnh và nội dung có thể tiếp tục được cập nhật.

## 📄 Bản quyền và tài nguyên

Các tài nguyên trong dự án có thể bao gồm mã nguồn, hình ảnh, âm thanh, phông chữ và dữ liệu từ nhiều nguồn khác nhau. Vui lòng kiểm tra quyền sử dụng và thông tin giấy phép của từng tài nguyên trước khi sao chép, chỉnh sửa hoặc phân phối lại.

---

<p align="center">
  <strong>HÀNH TRÌNH HUY HIỆU – BADGE JOURNEY</strong><br>
  <em>Chơi để khám phá – Học để vươn xa.</em>
</p>
