from __future__ import annotations

from typing import Any, Dict

from backend.services.fake_image_detector import analyze_image
from backend.services.image_region_analysis import analyse_image_regions
from backend.services.image_visual_evidence import (
    generate_image_visual_evidence,
)


def _safe_result(
    result: Any,
) -> Dict[str, Any]:
    """
    Ensures the base image detector returned a valid dictionary.
    """

    if not isinstance(result, dict):
        return {
            "error": (
                "The image detector returned an invalid response."
            )
        }

    return result


def _build_visual_evidence_response(
    visual_evidence: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Removes internal filesystem paths from the API response and
    exposes only frontend-accessible URLs and interpretation metadata.
    """

    return {
        "heatmap": visual_evidence.get(
            "heatmap_url"
        ),
        "overlay": visual_evidence.get(
            "overlay_url"
        ),
        "naturalness_map": visual_evidence.get(
            "naturalness_url"
        ),
        "edge_map": visual_evidence.get(
            "edge_map_url"
        ),
        "frequency_map": visual_evidence.get(
            "frequency_map_url"
        ),
        "legend": visual_evidence.get(
            "legend",
            {
                "blue": "Strongly natural region",
                "cyan": "Likely natural region",
                "green": "Mostly natural region",
                "yellow": "Mixed or uncertain region",
                "orange": "Suspicious synthetic indicator",
                "red": "Strong AI or manipulation indicator",
            },
        ),
        "interpretation_notice": visual_evidence.get(
            "interpretation_notice",
            (
                "Red and orange regions contain stronger "
                "forensic irregularities. Green, cyan and blue "
                "regions show more natural image characteristics."
            ),
        ),
    }


def process_image(
    image_path: str,
) -> Dict[str, Any]:
    """
    Complete FORGE image-processing pipeline.

    Processing order:
        1. Run the existing CNN + Random Forest detector.
        2. Generate explainable visual evidence.
        3. Generate semantic-region and patch-level analysis.
        4. Merge all outputs into one frontend-compatible response.

    The base prediction models are not modified here.
    """

    try:
        # =====================================================
        # 1. BASE IMAGE DETECTOR
        # CNN + RANDOM FOREST + HANDCRAFTED FEATURES
        # =====================================================

        base_result = analyze_image(
            image_path
        )

        result = _safe_result(
            base_result
        )

        if result.get("error"):
            return result

        # =====================================================
        # 2. VISUAL FORENSIC EVIDENCE
        # HEATMAP + OVERLAY + NATURALNESS + EDGE + FREQUENCY
        # =====================================================

        visual_evidence = (
            generate_image_visual_evidence(
                image_path
            )
        )

        if not isinstance(
            visual_evidence,
            dict,
        ):
            return {
                "error": (
                    "Visual evidence generator returned "
                    "an invalid response."
                )
            }

        # The internal heatmap path is required by the
        # regional-analysis engine.
        heatmap_path = visual_evidence.get(
            "heatmap_path"
        )

        # =====================================================
        # 3. REGION + PATCH INVESTIGATION
        # =====================================================

        region_analysis = (
            analyse_image_regions(
                image_path=image_path,
                heatmap_path=heatmap_path,
            )
        )

        if not isinstance(
            region_analysis,
            dict,
        ):
            region_analysis = {
                "face_detected": False,
                "regions": [],
                "ranked_regions": [],
                "hover_grid": {
                    "patches": [],
                    "ranked_patches": [],
                },
                "error": (
                    "Regional investigation engine returned "
                    "an invalid response."
                ),
            }

        hover_analysis = (
            region_analysis.get(
                "hover_grid"
            )
            or {
                "patches": [],
                "ranked_patches": [],
            }
        )

        # =====================================================
        # 4. FRONTEND-SAFE VISUAL RESPONSE
        # =====================================================

        frontend_visuals = (
            _build_visual_evidence_response(
                visual_evidence
            )
        )

        # =====================================================
        # 5. MODEL PROBABILITY NORMALISATION
        # =====================================================

        raw_ai_probability = result.get(
            "raw_ai_probability"
        )

        raw_human_probability = result.get(
            "raw_human_probability"
        )

        if raw_ai_probability is None:
            raw_ai_probability = result.get(
                "raw_probability_fake"
            )

        if raw_human_probability is None:
            raw_human_probability = result.get(
                "raw_probability_real"
            )

        if raw_ai_probability is None:
            raw_ai_probability = result.get(
                "risk_score",
                0,
            )

        try:
            ai_probability = float(
                raw_ai_probability or 0
            )

            if 0 <= ai_probability <= 1:
                ai_probability *= 100

            ai_probability = max(
                0.0,
                min(
                    100.0,
                    ai_probability,
                ),
            )

        except (
            TypeError,
            ValueError,
        ):
            ai_probability = 0.0

        if raw_human_probability is None:
            human_probability = (
                100.0 - ai_probability
            )

        else:
            try:
                human_probability = float(
                    raw_human_probability
                )

                if 0 <= human_probability <= 1:
                    human_probability *= 100

                human_probability = max(
                    0.0,
                    min(
                        100.0,
                        human_probability,
                    ),
                )

            except (
                TypeError,
                ValueError,
            ):
                human_probability = (
                    100.0 - ai_probability
                )

        # =====================================================
        # 6. MERGE COMPLETE RESPONSE
        # =====================================================

        result.update(
            {
                # Backward-compatible field used by the
                # existing ImageVisuals component.
                "heatmap": frontend_visuals.get(
                    "overlay"
                ),

                # New full visual-evidence object.
                "visual_evidence": (
                    frontend_visuals
                ),

                # Semantic regions:
                # forehead, eyes, nose, cheeks, mouth, jaw,
                # or fallback image quadrants.
                "region_analysis": (
                    region_analysis
                ),

                # Patch-level hover data used by
                # InteractiveImageInvestigator.jsx.
                "hover_analysis": (
                    hover_analysis
                ),

                # Standard modality fields.
                "file_type": "image",
                "modality": "image",

                # Standard probability contract.
                "probabilities": {
                    "ai": round(
                        ai_probability,
                        2,
                    ),
                    "human": round(
                        human_probability,
                        2,
                    ),
                },

                # Pipeline version information.
                "image_analysis_version": (
                    "FORGE-IMAGE-INVESTIGATION-2.1"
                ),

                "visual_evidence_version": (
                    "FORGE-VISUAL-XAI-2.1"
                ),

                "regional_analysis_version": (
                    region_analysis.get(
                        "analysis_version",
                        "FORGE-IMAGE-REGION-XAI",
                    )
                ),
            }
        )

        # =====================================================
        # 7. OPTIONAL SUMMARY FOR FRONTEND / REPORT
        # =====================================================

        ranked_regions = (
            region_analysis.get(
                "ranked_regions"
            )
            or []
        )

        ranked_patches = (
            hover_analysis.get(
                "ranked_patches"
            )
            or []
        )

        most_suspicious_region = (
            ranked_regions[0]
            if ranked_regions
            else None
        )

        most_suspicious_patch = (
            ranked_patches[0]
            if ranked_patches
            else None
        )

        result[
            "image_investigation_summary"
        ] = {
            "face_detected": (
                region_analysis.get(
                    "face_detected",
                    False,
                )
            ),
            "semantic_region_count": len(
                region_analysis.get(
                    "regions",
                    [],
                )
            ),
            "hover_patch_count": len(
                hover_analysis.get(
                    "patches",
                    [],
                )
            ),
            "most_suspicious_region": (
                most_suspicious_region
            ),
            "most_suspicious_patch": (
                most_suspicious_patch
            ),
            "interpretation": (
                frontend_visuals.get(
                    "interpretation_notice"
                )
            ),
        }

        return result

    except Exception as error:
        return {
            "error": (
                "Image pipeline failed: "
                f"{str(error)}"
            ),
            "modality": "image",
            "file_type": "image",
        }