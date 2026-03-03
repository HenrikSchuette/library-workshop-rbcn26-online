*** Settings ***
Library    hybrid.minicart_hybrid.MiniCartHybridLibrary    kw_group=pricing

*** Test Cases ***
Only Pricing Keywords Are Available
    # These should work:
    ${disc}=    Apply Discount   100    10
    ${total}=   Total With Tax   ${disc}   21
    Should Be Equal As Numbers   ${total}   108.9

    # And a non-pricing keyword should NOT be available:
    Run Keyword And Expect Error    *No keyword with name*Add Line Item*    Add Line Item    10    1
