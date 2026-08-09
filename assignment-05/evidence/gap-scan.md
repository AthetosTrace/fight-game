# Gap scan

| | |
|---|---|
| Requirements parsed | 63 steps, 178 assets |
| Assets found in the build | 184 |
| Steps with something missing | 59 |

**Selected to build: `M1-21` - Gray-box L_ShatteredRing**

Highest-ranked gap that falls inside this side's ownership. Everything ranked above it belongs to the gameplay owner.

## Ranked gaps

Ranked by blocking step: the lowest-numbered build step that cannot execute until the gap is closed.

| Rank | Step | What it produces | Missing | Ours |
|---|---|---|---|---|
| 1 | `M1-05` | Create DA_TuningGlobals | `DA_TuningGlobals` | no |
| 2 | `M1-06` | Create BP_PresentationSubsystem (wired and EMPTY) | `BP_PresentationSubsystem` | no |
| 3 | `M1-07` | Create WBP_DebugPanel | `WBP_DebugPanel` | no |
| 4 | `M1-08` | Create the shared BP_HealthComponent | `BP_HealthComponent` | no |
| 5 | `M1-09` | Create BP_DuelDirector | `BP_DuelDirector`, `DA_FighterProfile` | no |
| 6 | `M1-10` | Create the Enhanced Input assets | `IMC_Duel`, `IA_LightAttack`, `IA_Dodge`, `IA_Counter`, `IA_LockOn`, `IA_Impact`, `IA_FinalClash` | no |
| 7 | `M1-11` | Create BP_PlayerFighter (the ONE player class) | `BP_Echo`, `BP_Nova`, `BP_HealthComponent`, `BP_CombatComponent`, `BP_AscensionComponent`, `BP_LockOnComponent` | no |
| 8 | `M1-12` | Create DA_FighterProfile + Echo and Nova instances | `DA_FighterProfile`, `DA_FighterProfile_Echo`, `DA_FighterProfile_Nova`, `ABP_Fighter` | no |
| 9 | `M1-13` | Implement ApplyFighterProfile | `BP_DuelDirector` | no |
| 10 | `M1-14` | Create ABP_Fighter (shared AnimBP with stance additive) | `ABP_Fighter`, `DA_FighterProfile` | no |
| 11 | `M1-15` | Create BP_CombatComponent | `BP_CombatComponent`, `ANS_ActiveHit` | no |
| 12 | `M1-16` | Create BP_LockOnComponent | `BP_LockOnComponent`, `IA_LockOn`, `WBP_HUD` | no |
| 13 | `M1-17` | Author AM_Player_LightCombo | `AM_Player_LightCombo`, `ANS_ComboLink`, `ANS_ActiveHit`, `AN_ComboFinisher` | no |
| 14 | `M1-18` | Create the player combat notify states / notify | `ANS_ComboLink`, `ANS_ActiveHit`, `AN_ComboFinisher` | no |
| 15 | `M1-19` | Author AM_Player_Dodge with nested i-frame notifies | `AM_Player_Dodge`, `ANS_IFrame`, `ANS_PerfectDodge` | no |
| 16 | `M1-20` | Wire the counter input and player counter montages | `AM_Player_Counter`, `AM_Player_CounterWhiff`, `IA_Counter`, `AM_Vanguard_CounterReact` | no |
| 17 | `M1-21` | Gray-box L_ShatteredRing | `L_ShatteredRing`, `PS_VanguardEntrance`, `PS_VanguardCombatMark` | yes |
| 18 | `M1-22` | Character-select entry | `WBP_CharacterSelect`, `L_CharacterSelect`, `DA_FighterProfile` | no |
| 19 | `M1-23` | Stand up the dressed proxies (asset selection, NOT presentation) | `DA_FighterProfile` | no |
| 20 | `M2-01` | Create the rival enums | `E_VanguardState`, `E_VanguardAttackID` | no |
| 21 | `M2-02` | Create S_AttackPhaseTuning | `S_AttackPhaseTuning` | no |
| 22 | `M2-03` | Create S_VanguardAttackDef | `E_VanguardAttackID`, `S_AttackPhaseTuning` | no |
| 23 | `M2-04` | Create DT_VanguardAttacks with all four rows | `DT_VanguardAttacks` | no |
| 24 | `M2-05` | Create BP_CrimsonVanguard | `BP_HealthComponent` | no |
| 25 | `M2-06` | Create BP_VanguardCombatComponent | `BP_VanguardCombatComponent`, `DT_VanguardAttacks`, `ANS_ActiveHit`, `ANS_Recover` | no |
| 26 | `M2-07` | Create BP_VanguardController (AIController) | `BP_VanguardController` | no |
| 27 | `M2-08` | Create BB_CrimsonVanguard (Blackboard) | `BB_CrimsonVanguard`, `E_VanguardState`, `E_VanguardAttackID` | no |
| 28 | `M2-09` | Build BT_CrimsonVanguard | `BT_CrimsonVanguard`, `BB_CrimsonVanguard`, `BTTask_WaitIndefinite`, `BTService_UpdateCombatData`, `BTService_DrawDebugState`, `BTTask_Idle_Reposition`, `BTTask_SelectAttack`, `BTTask_Telegraph`, `BTTask_ActiveAttack`, `BTTask_Recover`, `BTTask_ReturnToNeutral` | no |
| 29 | `M2-10` | Create BTService_UpdateCombatData | `BTService_UpdateCombatData` | no |
| 30 | `M2-11` | Create BTService_DrawDebugState | `BTService_DrawDebugState` | no |
| 31 | `M2-12` | Create the six BTTask_* tasks | `BTTask_Idle_Reposition`, `BTTask_SelectAttack`, `BTTask_Telegraph`, `BTTask_ActiveAttack`, `ANS_ActiveHit`, `ANS_TrackingLock`, `BTTask_Recover`, `ANS_Recover`, `BTTask_ReturnToNeutral` | no |
| 32 | `M2-13` | Author Attack A montage and its notify states | `AM_Vanguard_AttackA`, `ANS_CounterWindow`, `ANS_Telegraph`, `ANS_ActiveHit`, `ANS_Recover` | no |
| 33 | `M2-14` | Wire the counter interrupt through the sequence | `BTTask_Recover`, `AM_Vanguard_CounterReact` | no |
| 34 | `M3-01` | Create the meter/impact enums | `E_MeterEvent`, `E_ImpactTrigger` | no |
| 35 | `M3-02` | Create S_MeterGain + DT_MeterGains (five rows) | `S_MeterGain`, `DT_MeterGains` | no |
| 36 | `M3-03` | Create BP_AscensionComponent | `BP_AscensionComponent`, `BP_FinalClashDirector` | no |
| 37 | `M3-04` | Create WBP_HUD (meter bar + reticle + gate indicators stub) | `WBP_HUD` | no |
| 38 | `M3-05` | Wire all five meter hooks | `AN_ComboFinisher`, `IA_Counter`, `ANS_CounterWindow`, `BP_ImpactWindowDirector` | no |
| 39 | `M3-06` | Create WBP_ImpactPrompt | `WBP_ImpactPrompt` | no |
| 40 | `M3-07` | Create BP_ImpactWindowDirector | `BP_ImpactWindowDirector`, `BP_DuelDirector`, `WBP_ImpactPrompt`, `IA_Impact` | no |
| 41 | `M3-08` | Write RestoreCombatState() once | `BP_DuelDirector`, `BP_PresentationSubsystem`, `WBP_ImpactPrompt`, `IA_Impact` | no |
| 42 | `M4-01` | Author Attacks B, C, and D | `AM_Vanguard_AttackB`, `AM_Vanguard_AttackC`, `AM_Vanguard_AttackD`, `ANS_Telegraph`, `ANS_ActiveHit`, `ANS_Recover`, `ANS_CounterWindow`, `DT_VanguardAttacks`, `ANS_TrackingLock` | no |
| 43 | `M4-02` | Create ANS_TrackingLock | `ANS_TrackingLock` | no |
| 44 | `M4-03` | Range- and cooldown-based selection across all four attacks | `BTTask_SelectAttack` | no |
| 45 | `M4-04` | Phase 2 via the one data path | `BP_DuelDirector`, `BTTask_ReturnToNeutral`, `BP_PresentationSubsystem` | no |
| 46 | `M4-05` | Create BP_FinalClashDirector and the double gate | `BP_FinalClashDirector`, `BP_DuelDirector`, `WBP_HUD`, `IA_FinalClash` | no |
| 47 | `M4-06` | The two timing beats (reuse 7 machinery) + LS_FinalClash | `LS_FinalClash`, `AM_Clash_Beat1`, `AM_Clash_Finisher`, `AM_Vanguard_CounterReact`, `BTTask_WaitIndefinite`, `IA_Impact`, `WBP_ImpactPrompt` | no |
| 48 | `M4-07` | Clash SUCCESS -> Win | `AM_Clash_Finisher`, `BP_HealthComponent`, `WBP_Result` | no |
| 49 | `M4-08` | Clash FAILURE -> the exact seven-step recovery | `LS_FinalClash`, `BTTask_WaitIndefinite` | no |
| 50 | `M4-09` | Loss condition and WBP_Result | `WBP_Result` | no |
| 51 | `M4-10` | LS_VanguardEntrance (abbreviated, skippable) | `LS_VanguardEntrance`, `PS_VanguardEntrance`, `PS_VanguardCombatMark`, `BP_PresentationSubsystem` | no |
| 52 | `M5-01` | Fill RequestHitStop / RequestTimeDilation (hit-stop & time-dilation tuning) | `BP_PresentationSubsystem` | no |
| 53 | `M5-02` | Fill RequestCameraShake + camera choreography | `BP_PresentationSubsystem` | no |
| 54 | `M5-03` | Fill RequestVFX with authored Niagara systems | `BP_PresentationSubsystem` | no |
| 55 | `M5-04` | Fill RequestSound + full sound design and mix | `BP_PresentationSubsystem` | no |
| 56 | `M5-05` | Arena environmental reaction (R6) | `L_ShatteredRing` | no |
| 57 | `M5-06` | Final character treatment for Echo, Nova, Crimson Vanguard | `DA_FighterProfile` | no |
| 58 | `M5-07` | Full-fidelity Final Clash choreography | `LS_FinalClash` | no |
| 59 | `M5-08` | The editorial character-selection interface | `WBP_CharacterSelect`, `DA_FighterProfile`, `L_ShatteredRing`, `DT_VanguardAttacks`, `BT_CrimsonVanguard`, `BP_PresentationSubsystem`, `ANS_Recover`, `ANS_ComboLink` | no |

## Aliases applied

Assets the sequence planned under one name and the prototype shipped under another.

| Planned | Shipped as | Why |
|---|---|---|
| `BP_CrimsonVanguard` | `BP_VanguardProxy` | The rival ships as a proxy actor driven by external movement and attack drivers, rather than the single self-contained Blueprint the sequence planned. |
| `BP_PlayerFighter` | `BP_ThirdPersonCharacter` | The prototype built the player on the Third Person template character rather than a fresh Blueprint. Same role, different asset name. |

