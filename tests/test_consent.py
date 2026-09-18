import pytest

from stylens.domain.models import ConsentRecord, ConsultationSession, SessionStatus


def test_explicit_adult_consent_advances_session() -> None:
    session = ConsultationSession()

    session.record_consent(
        ConsentRecord(notice_version="1.0", accepted=True, adult_confirmed=True)
    )

    assert session.status is SessionStatus.CONSENTED


@pytest.mark.parametrize(
    ("accepted", "adult_confirmed"),
    [(False, True), (True, False), (False, False)],
)
def test_invalid_consent_is_rejected(accepted: bool, adult_confirmed: bool) -> None:
    session = ConsultationSession()

    with pytest.raises(ValueError, match="Explicit adult consent"):
        session.record_consent(
            ConsentRecord(
                notice_version="1.0",
                accepted=accepted,
                adult_confirmed=adult_confirmed,
            )
        )

