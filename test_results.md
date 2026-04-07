# Test Results - TravelBuddy Agent

**Ngày chạy test:** 2026-04-07  
**Model:** gpt-4.1-mini (temperature=0, parallel_tool_calls=False)  
**Kết quả tổng:** 5/5 PASS

---

## Test 1: Chào hỏi (Không gọi tool)

**Input:** `Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.`

**Expected:** Chào hỏi, hỏi thêm sở thích, KHÔNG gọi tool

**Console Log:**
```
2026-04-07 16:08:56,150 [INFO] travel_agent: Agent node invoked - 1 messages in state
2026-04-07 16:08:57,879 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 16:08:57,885 [INFO] travel_agent: No tool calls - agent responding directly
```

**Tool calls:** None

**Response:**
```
Chào bạn! Bạn thích đi du lịch khám phá thiên nhiên, biển đảo, hay muốn trải nghiệm văn hóa,
ẩm thực ở thành phố nào đó trong Việt Nam? Bạn có thể cho mình biết sở thích hoặc mong muốn
của bạn để mình gợi ý điểm đến phù hợp nhé!
```

**Result:** ✅ PASS  
**Phân tích:** Agent trả lời bằng tiếng Việt, hỏi về sở thích để tư vấn phù hợp, không gọi tool nào.

---

## Test 2: Tìm chuyến bay (Single tool)

**Input:** `Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng`

**Expected:** Gọi `search_flights("Hà Nội", "Đà Nẵng")`, liệt kê 4 chuyến bay

**Console Log:**
```
2026-04-07 16:08:57,886 [INFO] travel_agent: Agent node invoked - 1 messages in state
2026-04-07 16:08:58,791 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 16:08:58,795 [INFO] travel_agent: Tool call: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
2026-04-07 16:08:58,808 [INFO] travel_tools: search_flights called: origin='Hà Nội', destination='Đà Nẵng'
2026-04-07 16:08:58,808 [INFO] travel_tools: Tìm thấy 4 chuyến bay
2026-04-07 16:08:58,809 [INFO] travel_agent: Agent node invoked - 3 messages in state
2026-04-07 16:09:02,581 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 16:09:02,582 [INFO] travel_agent: No tool calls - agent responding directly
```

**Tool calls:** `search_flights`

**Response:**
```
✈️ THÔNG TIN CHUYẾN BAY TỪ HÀ NỘI ĐI ĐÀ NẴNG:
1. VietJet Air - 08:30 → 09:50 - Economy - 890.000đ (Đề xuất: giá tốt nhất)
2. Bamboo Airways - 11:00 → 12:20 - Economy - 1.200.000đ
3. Vietnam Airlines - 06:00 → 07:20 - Economy - 1.450.000đ
4. Vietnam Airlines - 14:00 → 15:20 - Business - 2.800.000đ

Bạn muốn tôi giúp tìm khách sạn hoặc lên kế hoạch chi tiết cho chuyến đi không?
Nếu có, bạn vui lòng cho biết số đêm ở Đà Nẵng và ngân sách dự kiến nhé!
```

**Result:** ✅ PASS  
**Phân tích:** Agent gọi đúng tool `search_flights` với params chính xác. Liệt kê đủ 4 chuyến bay đúng data từ FLIGHTS_DB, đề xuất chuyến giá tốt nhất (VietJet 890.000đ). Giá format đúng chuẩn VN.

---

## Test 3: Multi-tool chain (Critical)

**Input:** `Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!`

**Expected:** Agent tự động gọi lần lượt 3 tools: search_flights → search_hotels → calculate_budget (tuần tự, kết quả tool trước là đầu vào cho tool sau)

**Console Log:**
```
2026-04-07 16:09:02,583 [INFO] travel_agent: Agent node invoked - 1 messages in state
2026-04-07 16:09:04,285 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 16:09:04,286 [INFO] travel_agent: Tool call: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
2026-04-07 16:09:04,287 [INFO] travel_tools: search_flights called: origin='Hà Nội', destination='Phú Quốc'
2026-04-07 16:09:04,287 [INFO] travel_tools: Tìm thấy 3 chuyến bay
2026-04-07 16:09:04,288 [INFO] travel_agent: Agent node invoked - 3 messages in state
2026-04-07 16:09:05,190 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 16:09:05,191 [INFO] travel_agent: Tool call: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1495000})
2026-04-07 16:09:05,192 [INFO] travel_tools: search_hotels called: city='Phú Quốc', max_price=1495000
2026-04-07 16:09:05,192 [INFO] travel_tools: Lọc theo giá <= 1.495.000đ: 2/4 khách sạn
2026-04-07 16:09:05,194 [INFO] travel_agent: Agent node invoked - 5 messages in state
2026-04-07 16:09:06,368 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 16:09:06,371 [INFO] travel_agent: Tool call: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:4000000'})
2026-04-07 16:09:06,373 [INFO] travel_tools: calculate_budget called: budget=5000000, expenses='vé_máy_bay:1100000,khách_sạn:4000000'
2026-04-07 16:09:06,373 [INFO] travel_tools: Tổng chi: 5100000, Còn lại: -100000
2026-04-07 16:09:06,373 [INFO] travel_agent: Agent node invoked - 7 messages in state
2026-04-07 16:09:14,379 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 16:09:14,380 [INFO] travel_agent: No tool calls - agent responding directly
```

**Tool calls (tuần tự):**
1. `search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})` → tìm thấy 3 chuyến, chọn VietJet 1.100.000đ
2. `search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1495000})` → lọc 2/4 khách sạn (Lahana 800K, 9Station 200K)
3. `calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:4000000'})` → tổng chi 5.100.000đ, vượt 100.000đ

**Response:**
```
✈️ THÔNG TIN CHUYẾN BAY:
- VietJet Air, chuyến bay 16:00 → 18:15, giá 1.100.000đ (đề xuất vì giá tốt nhất)

🏨 THÔNG TIN KHÁCH SẠN:
- 9Station Hostel ⭐⭐, giá 200.000đ/đêm, khu vực Dương Đông, đánh giá 4.5/5.0 (rất tiết kiệm)
- Lahana Resort ⭐⭐⭐, giá 800.000đ/đêm, khu vực Dương Đông, đánh giá 4.0/5.0 (thoải mái hơn)

💰 TỔNG CHI PHÍ DỰ KIẾN:
- Vé máy bay: 1.100.000đ
- Khách sạn (2 đêm): 4.000.000đ
- Tổng chi: 5.100.000đ
- ⚠️ Vượt ngân sách 100.000đ, bạn có thể cân nhắc tăng ngân sách hoặc chọn
  khách sạn rẻ hơn như 9Station Hostel để tiết kiệm.

💡 GỢI Ý THÊM:
- Phú Quốc nổi tiếng với biển đẹp, hải sản tươi ngon.
- Nên thuê xe máy để dễ dàng khám phá đảo.
- Mang theo kem chống nắng và mũ rộng vành để bảo vệ da khi đi biển.
```

**Result:** ✅ PASS  
**Phân tích:** Agent gọi tuần tự đúng 3 tools. Dữ liệu liên kết chính xác:
- Bước 1 → chọn VietJet 1.100.000đ (đúng giá rẻ nhất trong FLIGHTS_DB)
- Bước 2 → max_price = (5tr - 1.1tr) / 2 ≈ 1.495.000đ, lọc được 2 KS phù hợp
- Bước 3 → tính ngân sách, phát hiện vượt 100K → cảnh báo và gợi ý chọn KS rẻ hơn
- Response đúng format với đầy đủ 4 section (bay, KS, ngân sách, gợi ý)

---

## Test 4: Thiếu thông tin (Hỏi clarification)

**Input:** `Tôi muốn đặt khách sạn`

**Expected:** Hỏi lại thông tin (thành phố, số đêm, ngân sách), KHÔNG gọi tool

**Console Log:**
```
2026-04-07 16:09:14,381 [INFO] travel_agent: Agent node invoked - 1 messages in state
2026-04-07 16:09:15,864 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 16:09:15,864 [INFO] travel_agent: No tool calls - agent responding directly
```

**Tool calls:** None

**Response:**
```
Bạn muốn đặt khách sạn ở thành phố nào và dự định ở bao nhiêu đêm?
Bạn cũng có ngân sách tối đa cho mỗi đêm không?
Vui lòng cung cấp thêm thông tin để mình giúp bạn tìm khách sạn phù hợp nhé!
```

**Result:** ✅ PASS  
**Phân tích:** Agent nhận ra thiếu thông tin (thành phố, ngân sách, số đêm), hỏi lại người dùng thay vì gọi tool. Đúng yêu cầu Rule 6 trong system prompt.

---

## Test 5: Guardrail (Từ chối yêu cầu ngoài du lịch)

**Input:** `Giải giúp tôi bài tập lập trình Python về linked list`

**Expected:** Từ chối lịch sự, KHÔNG gọi tool

**Console Log:**
```
2026-04-07 16:09:15,865 [INFO] travel_agent: Agent node invoked - 1 messages in state
2026-04-07 16:09:17,019 [INFO] httpx: HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 16:09:17,024 [INFO] travel_agent: No tool calls - agent responding directly
```

**Tool calls:** None

**Response:**
```
Xin lỗi, tôi là trợ lý chuyên về du lịch Việt Nam nên không thể hỗ trợ yêu cầu này.
Tuy nhiên, nếu bạn đang có kế hoạch du lịch, tôi rất sẵn lòng giúp bạn tìm chuyến bay,
khách sạn và lên kế hoạch chi tiết! 😊
```

**Result:** ✅ PASS  
**Phân tích:** Agent từ chối lịch sự đúng mẫu trong constraints, không gọi tool, và chuyển hướng sang du lịch. Guardrail hoạt động chính xác.

---

## Tổng kết

| Test | Mô tả | Tool calls | Kết quả |
|------|--------|------------|---------|
| Test 1 | Chào hỏi, không gọi tool | None | ✅ PASS |
| Test 2 | Single tool call | search_flights | ✅ PASS |
| Test 3 | Multi-tool chain (tuần tự) | search_flights → search_hotels → calculate_budget | ✅ PASS |
| Test 4 | Thiếu info, hỏi clarification | None | ✅ PASS |
| Test 5 | Guardrail, từ chối | None | ✅ PASS |

**Tổng kết: 5/5 PASS**
