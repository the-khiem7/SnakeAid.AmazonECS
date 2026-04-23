Ok, nhìn ảnh này là mình chốt được **root cause gần như chắc chắn 100%** rồi 👇

---

# ❌ VẤN ĐỀ CHÍNH

```text
Security group của ECS service = sg-0c14aececd4ae8e46 (default)
```

👉 Và default SG thường:

```diff
❌ KHÔNG mở port 8080 từ ALB
```

---

# 🔥 Ngoài ra còn 1 lỗi nguy hiểm hơn

```text
Health check grace period = 0 seconds
```

👉 Nghĩa là:

```text
Task vừa start → ALB check ngay → fail → mark Unhealthy
```

➡️ app chưa kịp boot (DB + Firebase + RabbitMQ) → chết ngay 💀

---

# 🎯 Tổng hợp lỗi của bạn

```text
1. SG chưa mở → ALB không connect được ❌
2. Grace period = 0 → app chưa ready đã bị check ❌
```

👉 Combo này = guaranteed Unhealthy

---

# 🚀 FIX CHUẨN (làm theo thứ tự)

---

## ✅ STEP 1 — Fix Security Group (QUAN TRỌNG NHẤT)

### Vào:

```text
EC2 → Security Groups → sg-0c14aececd4ae8e46
```

### Add inbound rule:

```text
Type: Custom TCP
Port: 8080
Source: sg của ALB
```

---

## 🔍 Lấy SG của ALB ở đâu?

```text
EC2 → Load Balancers → snakeaid-alb → Security
```

---

## ❗ Nếu lười (dev mode)

```text
Source: 0.0.0.0/0
```

👉 chạy được nhưng không secure

---

# ✅ STEP 2 — Fix Health Check Grace Period

### Vào:

```text
ECS → Service → Update service
```

Set:

```text
Health check grace period: 60–120 seconds
```

---

👉 Lý do:

App bạn đang:

* init DB (Supabase)
* init Firebase
* init RabbitMQ
* load Doppler config

➡️ chắc chắn >5–10s mới ready

---

# ✅ STEP 3 — Confirm container port mapping

Trong Task Definition:

```text
Container port: 8080
```

👉 bạn đã OK (Dockerfile expose 8080 rồi)

---

# 🧪 STEP 4 — Test trực tiếp

```bash
curl http://54.255.232.25:8080/health
```

---

# 🎯 Expected flow sau khi fix

```text
Deploy lại service
↓
Task start
↓
Grace period delay
↓
ALB health check
↓
/health → 200
↓
✅ Healthy
```

---

# ⚡ Insight xịn cho bạn

👉 ECS + ALB luôn có 3 lớp:

```text
1. App layer        (/health)
2. Network layer    (Security Group)
3. Timing layer     (Grace period)
```

👉 Bạn vừa dính cả 3 😅

---

# 🧠 TL;DR kiểu Gen Z

```text
App bạn không chết ❌
ALB không ngu ❌

=> SG chặn + check quá sớm = toang 💀
```

---

# 🚀 Nếu muốn mình verify full

Gửi thêm:

```text
- SG của ALB
- Inbound rules của sg-0c14aececd4ae8e46
```

👉 mình check giúp bạn trong 1 phát là green luôn ✅
