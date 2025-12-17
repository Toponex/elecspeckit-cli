"""
跨平台 API 密钥加密存储工具

实现 FR-044: 使用平台特定的密钥管理机制加密存储 API 密钥
- Windows: DPAPI (Data Protection API)
- Linux: keyring (libsecret/SecretService)
- macOS: Keychain

使用方法:
    from elecspeckit_init.crypto_utils import encrypt_api_key, decrypt_api_key

    # 加密密钥
    encrypted = encrypt_api_key("mouser-component-search", "my_api_key_value")

    # 解密密钥
    plaintext = decrypt_api_key("mouser-component-search", encrypted)
"""

import platform
import base64
import json
from typing import Optional

# 检测操作系统
_system = platform.system()


def encrypt_api_key(skill_name: str, api_key: str) -> str:
    """
    使用平台特定的密钥管理机制加密 API 密钥

    Args:
        skill_name: Skill 名称（用作密钥标识符）
        api_key: 明文 API 密钥

    Returns:
        加密后的 API 密钥（Base64 编码字符串）

    Raises:
        RuntimeError: 如果平台不支持或加密失败
    """
    if not api_key:
        return ""

    if _system == "Windows":
        return _encrypt_windows(skill_name, api_key)
    elif _system == "Darwin":  # macOS
        return _encrypt_macos(skill_name, api_key)
    elif _system == "Linux":
        return _encrypt_linux(skill_name, api_key)
    else:
        raise RuntimeError(f"不支持的操作系统: {_system}")


def decrypt_api_key(skill_name: str, encrypted_key: str) -> str:
    """
    使用平台特定的密钥管理机制解密 API 密钥

    Args:
        skill_name: Skill 名称（用作密钥标识符）
        encrypted_key: 加密后的 API 密钥（Base64 编码字符串）

    Returns:
        明文 API 密钥

    Raises:
        RuntimeError: 如果平台不支持或解密失败
    """
    if not encrypted_key:
        return ""

    if _system == "Windows":
        return _decrypt_windows(skill_name, encrypted_key)
    elif _system == "Darwin":  # macOS
        return _decrypt_macos(skill_name, encrypted_key)
    elif _system == "Linux":
        return _decrypt_linux(skill_name, encrypted_key)
    else:
        raise RuntimeError(f"不支持的操作系统: {_system}")


# ============================================================================
# Windows 实现 (DPAPI)
# ============================================================================

def _encrypt_windows(skill_name: str, api_key: str) -> str:
    """使用 Windows DPAPI 加密 API 密钥"""
    try:
        import win32crypt
    except ImportError:
        raise RuntimeError(
            "Windows DPAPI 加密需要 pywin32 库，请运行: uv pip install pywin32"
        )

    try:
        # 将字符串转换为字节
        plaintext_bytes = api_key.encode('utf-8')

        # 使用 DPAPI 加密（用户级别，无需额外密钥）
        encrypted_bytes = win32crypt.CryptProtectData(
            plaintext_bytes,
            f"ElecSpeckit-{skill_name}",  # 描述信息
            None,  # 可选熵（额外随机性）
            None,  # 保留
            None,  # 提示结构
            0      # 标志（0 = 用户级别）
        )

        # Base64 编码返回
        return base64.b64encode(encrypted_bytes).decode('ascii')
    except Exception as e:
        raise RuntimeError(f"Windows DPAPI 加密失败: {e}")


def _decrypt_windows(skill_name: str, encrypted_key: str) -> str:
    """使用 Windows DPAPI 解密 API 密钥"""
    try:
        import win32crypt
    except ImportError:
        raise RuntimeError(
            "Windows DPAPI 解密需要 pywin32 库，请运行: uv pip install pywin32"
        )

    try:
        # Base64 解码
        encrypted_bytes = base64.b64decode(encrypted_key.encode('ascii'))

        # 使用 DPAPI 解密
        plaintext_bytes = win32crypt.CryptUnprotectData(
            encrypted_bytes,
            None,  # 保留
            None,  # 可选熵
            None,  # 保留
            0      # 标志
        )[1]  # 返回值是 (description, plaintext)

        # 转换为字符串
        return plaintext_bytes.decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Windows DPAPI 解密失败: {e}")


# ============================================================================
# macOS 实现 (Keychain)
# ============================================================================

def _encrypt_macos(skill_name: str, api_key: str) -> str:
    """使用 macOS Keychain 存储 API 密钥"""
    try:
        import keyring
    except ImportError:
        raise RuntimeError(
            "macOS Keychain 加密需要 keyring 库，请运行: uv pip install keyring"
        )

    try:
        # 存储到 Keychain（服务名：ElecSpeckit，账户名：skill_name）
        keyring.set_password("ElecSpeckit", skill_name, api_key)

        # 返回标记（表示已存储到 Keychain）
        marker = {
            "type": "keychain",
            "service": "ElecSpeckit",
            "account": skill_name
        }
        return base64.b64encode(json.dumps(marker).encode('utf-8')).decode('ascii')
    except Exception as e:
        raise RuntimeError(f"macOS Keychain 存储失败: {e}")


def _decrypt_macos(skill_name: str, encrypted_key: str) -> str:
    """从 macOS Keychain 读取 API 密钥"""
    try:
        import keyring
    except ImportError:
        raise RuntimeError(
            "macOS Keychain 解密需要 keyring 库，请运行: uv pip install keyring"
        )

    try:
        # 从 Keychain 读取（服务名：ElecSpeckit，账户名：skill_name）
        api_key = keyring.get_password("ElecSpeckit", skill_name)

        if api_key is None:
            raise RuntimeError(f"未找到 Skill '{skill_name}' 的 API 密钥")

        return api_key
    except Exception as e:
        raise RuntimeError(f"macOS Keychain 读取失败: {e}")


# ============================================================================
# Linux 实现 (keyring/libsecret)
# ============================================================================

def _encrypt_linux(skill_name: str, api_key: str) -> str:
    """使用 Linux keyring (libsecret) 存储 API 密钥"""
    try:
        import keyring
    except ImportError:
        raise RuntimeError(
            "Linux keyring 加密需要 keyring 库，请运行: uv pip install keyring\n"
            "并确保已安装 libsecret: sudo apt install libsecret-1-0 (Ubuntu/Debian)"
        )

    try:
        # 存储到 keyring（服务名：ElecSpeckit，账户名：skill_name）
        keyring.set_password("ElecSpeckit", skill_name, api_key)

        # 返回标记（表示已存储到 keyring）
        marker = {
            "type": "keyring",
            "service": "ElecSpeckit",
            "account": skill_name
        }
        return base64.b64encode(json.dumps(marker).encode('utf-8')).decode('ascii')
    except Exception as e:
        raise RuntimeError(f"Linux keyring 存储失败: {e}")


def _decrypt_linux(skill_name: str, encrypted_key: str) -> str:
    """从 Linux keyring (libsecret) 读取 API 密钥"""
    try:
        import keyring
    except ImportError:
        raise RuntimeError(
            "Linux keyring 解密需要 keyring 库，请运行: uv pip install keyring\n"
            "并确保已安装 libsecret: sudo apt install libsecret-1-0 (Ubuntu/Debian)"
        )

    try:
        # 从 keyring 读取（服务名：ElecSpeckit，账户名：skill_name）
        api_key = keyring.get_password("ElecSpeckit", skill_name)

        if api_key is None:
            raise RuntimeError(f"未找到 Skill '{skill_name}' 的 API 密钥")

        return api_key
    except Exception as e:
        raise RuntimeError(f"Linux keyring 读取失败: {e}")


# ============================================================================
# 工具函数
# ============================================================================

def is_encrypted(value: str) -> bool:
    """
    检查字符串是否为加密后的 API 密钥

    Args:
        value: 待检查的字符串

    Returns:
        True 如果是加密密钥，False 否则
    """
    if not value:
        return False

    # 检查是否为 Base64 编码
    try:
        decoded = base64.b64decode(value.encode('ascii'))

        # 尝试解析为 JSON（macOS/Linux 的标记）
        try:
            marker = json.loads(decoded.decode('utf-8'))
            if isinstance(marker, dict) and "type" in marker:
                return True
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

        # Windows DPAPI 加密数据通常较长（>100 字节）
        if len(decoded) > 100:
            return True

        return False
    except Exception:
        return False


def migrate_plaintext_to_encrypted(skill_config_path: str) -> int:
    """
    将 skill_config.json 中的明文 API 密钥迁移到加密存储

    Args:
        skill_config_path: skill_config.json 文件路径

    Returns:
        迁移的密钥数量

    Raises:
        FileNotFoundError: 如果配置文件不存在
        json.JSONDecodeError: 如果配置文件格式错误
    """
    import os

    if not os.path.exists(skill_config_path):
        raise FileNotFoundError(f"配置文件不存在: {skill_config_path}")

    # 读取配置文件
    with open(skill_config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    migrated_count = 0

    # 遍历所有 Skills
    for skill_name, skill_config in config.get("skills", {}).items():
        api_key = skill_config.get("api_key", "")

        # 跳过空密钥和已加密密钥
        if not api_key or is_encrypted(api_key):
            continue

        try:
            # 加密密钥
            encrypted_key = encrypt_api_key(skill_name, api_key)

            # 更新配置
            skill_config["api_key"] = encrypted_key

            migrated_count += 1
        except Exception as e:
            print(f"警告: 无法加密 Skill '{skill_name}' 的 API 密钥: {e}")
            continue

    # 写回配置文件
    if migrated_count > 0:
        # 创建备份
        backup_path = skill_config_path + ".plaintext.bak"
        import shutil
        shutil.copy(skill_config_path, backup_path)

        # 写入加密后的配置
        with open(skill_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        print(f"已迁移 {migrated_count} 个 API 密钥到加密存储")
        print(f"原配置已备份到: {backup_path}")

    return migrated_count
