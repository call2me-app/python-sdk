"""SDK'nın çağırdığı her uç CANLI API'de var olmalı.

ÖLÇÜLEN KUSURLAR (4 Eki 2026, canlı `openapi.json`'a karşı doğrulandı):

  SDK çağırıyor                              Gerçek
  POST /v1/knowledge-base/{id}/sources   →   .../add-sources
  PATCH /v1/api-keys/{id}/revoke         →   DELETE /v1/api-keys/{id}
  POST /v1/phone-numbers/{n}/unbind      →   DELETE (metot yanlış)
  GET  /v1/payments/saved-cards          →   GET /v1/payments/methods
  GET  /v1/voices/providers              →   hiç yok

Beşi de README'de ÖRNEK olarak duruyordu: kopyalayan kullanıcı 404 alır.

Spec ÇEVRİMDIŞI kopyadan okunuyor (`tests/openapi.json`): ağ yoksa test
atlanmaz, yanlış geçmez. Kopya eskirse `scripts/` ile tazelenir.
"""
from __future__ import annotations

import json
import pathlib
import re

import pytest

KOK = pathlib.Path(__file__).resolve().parents[1]
SPEC = KOK / "tests" / "openapi.json"
ISTEMCI = KOK / "call2me" / "client.py"


def _yollar() -> set[tuple[str, str]]:
    spec = json.loads(SPEC.read_text())
    norm = lambda s: re.sub(r"\{[^}]+\}", "{}", s)
    return {
        (m.upper(), norm(y))
        for y, v in spec.get("paths", {}).items()
        for m in v
        if m in ("get", "post", "put", "patch", "delete")
    }


def _sdk_cagrilari() -> list[tuple[str, str, int]]:
    """`self._http.<metot>("/v1/...")` çağrılarını çıkar."""
    out = []
    for i, satir in enumerate(ISTEMCI.read_text().splitlines(), 1):
        # ⚠️ İLK DESENİM HİÇBİR ŞEY YAKALAMIYORDU (`_http.post(...)` aradı)
        # ve test 5 ölü uç varken YEŞİL geçti. Gerçek biçim: `self._post(...)`.
        # `assert cagrilar` bu yüzden var — desen bozulursa testin sessizce
        # boşa dönmesini engelliyor.
        m = re.search(r'self\._(get|post|put|patch|delete)\(\s*f?"(/v1/[^"]*)"', satir)
        if m:
            yol = re.sub(r"\{[^}]+\}", "{}", m.group(2))
            out.append((m.group(1).upper(), yol, i))
    return out


def test_sdk_ucu_SPECTE_var():
    spec = _yollar()
    cagrilar = _sdk_cagrilari()
    assert cagrilar, "client.py'den hiç çağrı çıkarılamadı — desen bozulmuş olabilir"
    olu = [(m, y, n) for m, y, n in cagrilar if (m, y) not in spec]
    assert not olu, "API'de OLMAYAN uçlar:\n" + "\n".join(
        f"  client.py:{n}  {m} {y}" for m, y, n in olu
    )


def test_all_ilan_edilen_isimler_IMPORT_edilebilir():
    """`__all__`'da olup import edilmeyen isim → `from call2me import X` patlar.

    Ölçüldü: `Agent`, `Call`, `KnowledgeBase` `__all__`'daydı ama
    `__init__.py` onları hiç çekmiyordu. PyPI 1.4.0'da da aynı hata.
    """
    import call2me

    eksik = [ad for ad in call2me.__all__ if not hasattr(call2me, ad)]
    assert not eksik, f"__all__'da ilan edilip import edilmeyen: {eksik}"


# ── Kapsam: kullanıcıya açık ürünler SDK'da olmalı ──────────────────────
# ÖLÇÜLDÜ (5 Eki 2026): 278 uçtan yalnız 83'ü kapsanıyordu. Tercümanın
# 11 ucunun HİÇBİRİ yoktu — oysa ürün sayfası, fiyat listesi ve MCP
# sunucusu onu baş ürün olarak anlatıyor. Uzantı (10 uç), numara satın
# alma (5), referans programı (10) da yoktu.
#
# `internal/*` ve `auth/*` KASITLI dışarıda: biri cron/webhook yüzeyi,
# diğeri oturum açma — ikisi de SDK kullanıcısının işi değil.

ACIK_URUNLER = {
    "interpreters": "tercüman (telefon + web görüşme)",
    "numbers": "numara arama ve satın alma",
    "sms": "SMS gönderme",
    "ext": "Chrome uzantısı",
}


def test_acik_urunlerin_hepsi_SDKda():
    kaynak = ISTEMCI.read_text(encoding="utf-8")
    eksik = [
        f"{alan} ({aciklama})"
        for alan, aciklama in ACIK_URUNLER.items()
        if f"/v1/{alan}" not in kaynak
    ]
    assert not eksik, "SDK'da OLMAYAN ürünler:\n  " + "\n  ".join(eksik)


def test_giden_arama_baslatilabiliyor():
    """`POST /v1/calls` — README'ler 'outbound' diyor, uç olmalı."""
    kaynak = ISTEMCI.read_text(encoding="utf-8")
    assert 'self._post("/v1/calls"' in kaynak, "giden arama başlatma yok"
