---
title: "WireGuard on pfSense: A Step-by-Step Guide for Android, iPhone, and macOS"
categories:
  - Networking
  - VPN
  - pfSense
tags:
  - WireGuard
  - pfSense
  - VPN
  - Network Security
image:
  path: /assets/media/networking/wireguard_pfsense_guide.png
---

This is a **step-by-step walkthrough** for setting up **WireGuard on pfSense** and configuring **Android, iPhone, and macOS clients**.

## **Step 1: Install WireGuard on pfSense**

1. **Log in to pfSense Web UI** (`https://your-pfsense-ip`).
2. **Go to** `System` → `Package Manager` → `Available Packages`.
3. **Search for "WireGuard"** and click **Install**.
4. **Wait** for the installation to complete.

## **Step 2: Configure WireGuard on pfSense**

### **1. Enable WireGuard and Create a New Tunnel**

1. **Go to** `VPN` → `WireGuard`.
2. Click **Add Tunnel** and set:

   - **Enable**: ✅ (Checked)
   - **Description**: `WireGuard VPN`
   - **Listen Port**: `51820` (default, change if needed)
   - **Interface Keys**:
     - Click **Generate** next to **Private Key** (this auto-generates the Public Key).
   - **Tunnel Address**:

     ```
     10.0.0.1/24
     ```

     (This is the VPN subnet, `10.0.0.1` is pfSense's WireGuard IP)

3. Click **Save Tunnel**.

### **2. Add Peers (Clients)**

For each device (Android, iPhone, MacBook), create a **Peer**.

1. Click **Edit** next to your tunnel.
2. Scroll to **Peers** → Click **Add Peer**.
3. Configure the **Peer**:

   - **Public Key**: (Will be generated from the client in Step 4)
   - **Allowed IPs**:

     ```
     10.0.0.2/32  # Android
     10.0.0.3/32  # iPhone
     10.0.0.4/32  # MacBook
     ```

     (Each device needs a unique VPN IP.)

   - **Persistent Keepalive**: `25` (prevents NAT timeout issues)

4. **Click Save & Apply Changes**.

### **3. Assign WireGuard as an Interface**

1. **Go to** `Interfaces` → `Assignments`.
2. Find the **WireGuard Tunnel** (`wg0`).
3. Click **Add** → Name it `WG`.
4. Click **Save & Apply Changes**.

### **4. Allow Traffic Through the Firewall**

1. **Go to** `Firewall` → `Rules` → **WG (WireGuard interface)**.
2. Click **Add** (to create a rule).
   - **Action**: Pass
   - **Interface**: `WG`
   - **Protocol**: Any
   - **Source**: `10.0.0.0/24`
   - **Destination**: `Any` (allows access to local and internet)
3. **Click Save & Apply**.

### **5. Allow VPN to Access Local Network**

1. **Go to** `Firewall` → `Rules` → `LAN`.
2. Click **Add** and set:
   - **Action**: Pass
   - **Protocol**: Any
   - **Source**: `10.0.0.0/24`
   - **Destination**: `192.168.0.0/24` (Your home LAN)
3. **Click Save & Apply**.

### **6. Enable Packet Forwarding**

1. **Go to** `System` → `Advanced` → `Firewall & NAT`.
2. **Check** `Enable Packet Forwarding`.
3. **Save & Apply**.

## **Step 3: Configure Clients (Android, iPhone, macOS)**

Each device needs:

1. A **private key** (generated on the client).
2. The **public key** sent to pfSense (Step 2.2).
3. A WireGuard **configuration file**.

### **1. Android Setup**

1. **Install** WireGuard from the [Google Play Store](https://play.google.com/store/apps/details?id=com.wireguard.android).
2. Open WireGuard → Click **+** → **Create from Scratch**.
3. Enter:

   ```
   [Interface]
   PrivateKey = (Generated on the tablet)
   Address = 10.0.0.2/24
   DNS = 192.168.0.1  # pfSense or your home DNS
   ```

4. **Add a Peer**:

   ```
   [Peer]
   PublicKey = (pfSense Public Key)
   Endpoint = your-public-ip:51820
   AllowedIPs = 192.168.0.0/24 # This is for split tunnelling
   PersistentKeepalive = 25
   ```

   > [!NOTE]
   > For full-tunnelling, specify `0.0.0.0/0` in the `AllowedIPs` filed.

5. **Click Save & Activate**.

### **2. iPhone Setup**

1. Install **WireGuard** from the [App Store](https://apps.apple.com/us/app/wireguard/id1441195209).
2. Open WireGuard → **Add a new tunnel**.
3. Enter the **same settings** as Android but use:
   - `Address = 10.0.0.3/24`
   - `AllowedIPs = 192.168.0.0/24`
4. **Save & Activate**.

### **3. macOS Setup**

1. Install **WireGuard** via Homebrew:

   ```
   brew install --cask wireguard-tools
   ```

2. Open WireGuard → **Create a new tunnel**.
3. Enter:

   ```
   [Interface]
   PrivateKey = (Generated on Mac)
   Address = 10.0.0.4/24
   DNS = 192.168.0.1

   [Peer]
   PublicKey = (pfSense Public Key)
   Endpoint = your-public-ip:51820
   AllowedIPs = 192.168.0.0/24
   PersistentKeepalive = 25
   ```

4. **Save & Activate**.

## **Step 4: Testing the VPN**

1. **Activate WireGuard on your devices**.
2. **Check connectivity**:
   - Ping your **router**: `ping 192.168.0.1`
   - Ping a **local device**: `ping 192.168.0.100`
   - Run `traceroute 192.168.0.1` (if needed).
3. **Check logs in pfSense**:
   - Go to `Status > System Logs > VPN (WireGuard)`.
   - Ensure your device **connects successfully**.

## **Step 5: Troubleshooting**

| Issue                             | Solution                                                   |
| --------------------------------- | ---------------------------------------------------------- |
| VPN connects but no access to LAN | Ensure firewall rules allow `10.0.0.0/24 → 192.168.0.0/24` |
| Can't reach internet              | Set `DNS = 192.168.0.1` in WireGuard config                |
| Connection drops frequently       | Increase `PersistentKeepalive = 25`                        |
| Can't connect                     | Check firewall logs for dropped packets                    |
| Bed address                       | Check the subnet configuration                             |

## **Conclusion**

This guide walks through **setting up WireGuard on pfSense** and connecting **Android, iPhone, and macOS** clients with **split tunneling**. After following these steps, your devices should have **secure remote access to your home network** without routing all internet traffic through the VPN.
