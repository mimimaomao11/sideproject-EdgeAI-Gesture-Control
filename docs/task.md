# Task Tracking Board

## 📌 Sprint 2: MediaPipe Integration (Current)

### To-Do
- [ ] Optimization: Smooth jittery landmarks (Optional)

### In Progress
- [ ] Refactor: Final code review before Sprint 3

### Done (Verification Required)
- [x] **Project Structure Refactoring** (Moved files to `src/`, `assets/`, `docs/`)
- [x] **MediaPipe Setup** (Integrated Tasks API)
- [x] **Hand Tracking** (Landmarks visualization implemented)
- [x] **Gesture Logic** (Basic count_fingers algorithm working)
- [x] **Documentation** (README updated to product-level)

---

## 📅 Sprint 1: Foundation (Completed)
- [x] Initialize Git Repository
- [x] Basic OpenCV Camera Setup
- [x] FPS Counter
- [x] OOP Class Structure

---

## 🔮 Sprint 3: IoT & MQTT (Planning)
**Goal:** Control a virtual light bulb using hand gestures.

1. **MQTT Infrastructure**
   - [ ] Install `paho-mqtt`
   - [ ] Setup local broker (Mosquitto) or use public test broker

2. **Command Logic**
   - [ ] Define JSON payload for commands
   - [ ] Implement `MQTTClient` class

3. **Integration**
   - [ ] Trigger MQTT publish on gesture change
   - [ ] Add cooldown timer (debounce) to prevent command spamming
