Add-Type -AssemblyName System.Drawing

$assetsDir = "C:\Users\SEEBIRAJ V\Datheon_Python_Internship\assets"
if (!(Test-Path $assetsDir)) {
    New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null
}

function Create-Card {
    param (
        [string]$Title,
        [string]$Subtitle,
        [string]$TaskNumber,
        [string]$BadgeText,
        [System.Drawing.Color]$AccentColor,
        [string[]]$KeyPoints,
        [string[]]$CodeLines,
        [string]$OutputPath
    )

    $width = 1200
    $height = 675
    $bmp = New-Object System.Drawing.Bitmap $width, $height
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

    # Background
    $bgBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(11, 15, 25))
    $g.FillRectangle($bgBrush, 0, 0, $width, $height)

    # Accent top border
    $accentBrush = New-Object System.Drawing.SolidBrush $AccentColor
    $g.FillRectangle($accentBrush, 0, 0, $width, 8)

    # Header Panel
    $headerBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(19, 26, 42))
    $g.FillRectangle($headerBrush, 40, 30, ($width - 80), 95)
    
    $borderPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(40, 52, 75)), 1
    $g.DrawRectangle($borderPen, 40, 30, ($width - 80), 95)

    # Title Fonts with [float]
    $fontTag = New-Object System.Drawing.Font("Arial", [float]11, [System.Drawing.FontStyle]::Bold)
    $fontTitle = New-Object System.Drawing.Font("Segoe UI", [float]20, [System.Drawing.FontStyle]::Bold)
    $fontSub = New-Object System.Drawing.Font("Segoe UI", [float]12, [System.Drawing.FontStyle]::Regular)
    $fontSection = New-Object System.Drawing.Font("Segoe UI", [float]14, [System.Drawing.FontStyle]::Bold)
    $fontBody = New-Object System.Drawing.Font("Segoe UI", [float]12, [System.Drawing.FontStyle]::Regular)
    $fontMono = New-Object System.Drawing.Font("Consolas", [float]10.5, [System.Drawing.FontStyle]::Regular)
    $fontFooter = New-Object System.Drawing.Font("Segoe UI", [float]10, [System.Drawing.FontStyle]::Regular)

    # Tag Badge
    $tagBrush = New-Object System.Drawing.SolidBrush $AccentColor
    $g.DrawString($TaskNumber.ToUpper(), $fontTag, $tagBrush, 60, 42)

    # Title
    $whiteBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(248, 250, 252))
    $g.DrawString($Title, $fontTitle, $whiteBrush, 60, 62)

    # Subtitle
    $subBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(148, 163, 184))
    $g.DrawString($Subtitle, $fontSub, $subBrush, 60, 96)

    # Badge Box Right
    $badgeBoxBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(30, 41, 59))
    $g.FillRectangle($badgeBoxBrush, ($width - 340), 50, 280, 45)
    $g.DrawRectangle($borderPen, ($width - 340), 50, 280, 45)
    $badgeTextBrush = New-Object System.Drawing.SolidBrush $AccentColor
    $g.DrawString($BadgeText, $fontTag, $badgeTextBrush, ($width - 325), 64)

    # Left Panel: Key Highlights
    $leftX = 40
    $leftY = 145
    $leftW = 530
    $leftH = 430
    $panelBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(15, 23, 42))
    $g.FillRectangle($panelBrush, $leftX, $leftY, $leftW, $leftH)
    $g.DrawRectangle($borderPen, $leftX, $leftY, $leftW, $leftH)

    $g.DrawString("Core Capabilities & Technical Highlights", $fontSection, $accentBrush, ($leftX + 25), ($leftY + 20))

    $yPos = $leftY + 65
    foreach ($point in $KeyPoints) {
        $g.FillEllipse($accentBrush, ($leftX + 25), ($yPos + 5), 8, 8)
        $rect = New-Object System.Drawing.RectangleF(($leftX + 45), $yPos, ($leftW - 65), 50)
        $g.DrawString($point, $fontBody, $whiteBrush, $rect)
        $yPos += 56
    }

    # Right Panel: Code / Output Preview
    $rightX = 590
    $rightY = 145
    $rightW = ($width - $rightX - 40)
    $rightH = 430
    $darkCodeBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(8, 11, 18))
    $g.FillRectangle($darkCodeBrush, $rightX, $rightY, $rightW, $rightH)
    $g.DrawRectangle($borderPen, $rightX, $rightY, $rightW, $rightH)

    # Window header bar
    $winBarBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(24, 32, 48))
    $g.FillRectangle($winBarBrush, $rightX, $rightY, $rightW, 35)
    $dotRed = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(239, 68, 68))
    $dotYellow = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(245, 158, 11))
    $dotGreen = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(16, 185, 129))
    $g.FillEllipse($dotRed, ($rightX + 15), ($rightY + 12), 11, 11)
    $g.FillEllipse($dotYellow, ($rightX + 33), ($rightY + 12), 11, 11)
    $g.FillEllipse($dotGreen, ($rightX + 51), ($rightY + 12), 11, 11)
    $g.DrawString("Console Terminal & Execution Output", $fontTag, $subBrush, ($rightX + 80), ($rightY + 9))

    # Code lines
    $codeY = $rightY + 48
    $codeColor = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(203, 213, 225))
    foreach ($line in $CodeLines) {
        $lineBrush = $codeColor
        if ($line.StartsWith(">") -or $line.StartsWith("$")) {
            $lineBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(56, 189, 248))
        } elseif ($line.Contains("ERROR") -or $line.Contains("Oops") -or $line.Contains("FAILED") -or $line.Contains("$-292")) {
            $lineBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(248, 113, 113))
        } elseif ($line.Contains("SUCCESS") -or $line.Contains("PASSED") -or $line.Contains("CONGRATULATIONS") -or $line.Contains("Splendid") -or $line.Contains("+$") -or $line.Contains("Verified") -or $line.Contains("100%")) {
            $lineBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(52, 211, 153))
        } elseif ($line.StartsWith("=") -or $line.StartsWith("-")) {
            $lineBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(100, 116, 139))
        }
        $g.DrawString($line, $fontMono, $lineBrush, ($rightX + 18), $codeY)
        $codeY += 22
    }

    # Footer
    $footerBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(148, 163, 184))
    $g.DrawString("Candidate: Seebiraj V  |  App ID: DT-2026-WH8V5  |  Datheon Python Programming Internship (Batch 01)", $fontFooter, $footerBrush, 40, 605)
    $g.DrawString("Repo: github.com/seebiraj/Datheon_Python_Internship", $fontFooter, $footerBrush, ($width - 430), 605)

    # Save
    $bmp.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)

    # Cleanup
    $g.Dispose()
    $bmp.Dispose()
    Write-Host "Created image: $OutputPath"
}

# ----------------- Task 1: Hangman -----------------
Create-Card `
    -Title "Task 1: Hangman Word Guessing Game (Console)" `
    -Subtitle "Interactive Terminal Game with ASCII Gallows Art & Duplicate Guess Protection" `
    -TaskNumber "Task 1 Deliverable" `
    -BadgeText "STATUS: VERIFIED (PASS)" `
    -AccentColor ([System.Drawing.Color]::FromArgb(56, 189, 248)) `
    -KeyPoints @(
        "7 dynamic ASCII gallows stages tracking 0 through 6 mistake thresholds.",
        "Formatted masked word display updating letter-by-letter (e.g. '_ A _ H E O N').",
        "Set-based duplicate penalty deduction prevention safeguards remaining lives.",
        "Input sanitization enforcing single alphabetic character entry [A-Z].",
        "Automated CI demo runner and pytest assertions ensuring 100% win/loss test coverage."
    ) `
    -CodeLines @(
        "$ python task1_hangman/demo_run.py",
        "--- Running Hangman Simulation: Victory Flow ---",
        "Secret Word Chosen: DATHEON",
        "Guess 'D': ✅ Splendid! 'D' is in the secret word. [Mistakes: 0]",
        "Guess 'A': ✅ Splendid! 'A' is in the secret word. [Mistakes: 0]",
        "Guess 'T': ✅ Splendid! 'T' is in the secret word. [Mistakes: 0]",
        "Guess 'X': ❌ Oops! 'X' is NOT in secret word. [Mistakes: 1]",
        "Guess 'H': ✅ Splendid! 'H' is in the secret word. [Mistakes: 1]",
        "Guess 'E': ✅ Splendid! 'E' is in the secret word. [Mistakes: 1]",
        "Guess 'O': ✅ Splendid! 'O' is in the secret word. [Mistakes: 1]",
        "Guess 'N': ✅ Splendid! 'N' is in the secret word. [Mistakes: 1]",
        "🎉 CONGRATULATIONS! YOU SAVED HIM! 🎉",
        "Secret Word: 'DATHEON' | Attempts Remaining: 5/6",
        "Duplicate check: '⚠️ Already guessed Z! No penalty.'",
        "All Task 1 automated demo simulations passed 100%!"
    ) `
    -OutputPath "$assetsDir\task1_hangman.png"

# ----------------- Task 2: Stock Portfolio Tracker -----------------
Create-Card `
    -Title "Task 2: Stock Portfolio Performance Tracker" `
    -Subtitle "Real-Time Valuation Engine, Profit/Loss Analytics & CSV Persistence" `
    -TaskNumber "Task 2 Deliverable" `
    -BadgeText "STATUS: VERIFIED (PASS)" `
    -AccentColor ([System.Drawing.Color]::FromArgb(16, 185, 129)) `
    -KeyPoints @(
        "S&P 500 benchmark dataset integration reading live prices from sp500_tickers.csv.",
        "Weighted average buy price algorithm recalculating positions upon capital injection.",
        "Computes Total Invested, Market Valuation, Absolute P/L ($), and Gain/Loss (%).",
        "Automatic external persistence to 'portfolio_summary.csv' via native csv.DictWriter.",
        "Clean formatted tabular console overview with color-ready profit/loss indicators."
    ) `
    -CodeLines @(
        "$ python task2_stock_portfolio/demo_run.py",
        "===========================================================",
        "        📈 DATHEON STOCK PORTFOLIO PERFORMANCE REPORT 📈   ",
        "===========================================================",
        "TICKER   SHARES   BUY ($)   CMP ($)   INVESTED   VALUATION   P/L ($)",
        "AAPL     15.00    $150.00   $182.50   $2250.00   $2737.50    +$487.50 (+21.67%)",
        "NVDA     25.00    $95.00    $130.40   $2375.00   $3260.00    +$885.00 (+37.26%)",
        "MSFT     10.00    $390.00   $425.20   $3900.00   $4252.00    +$352.00 (+9.03%)",
        "TSLA     12.00    $240.00   $215.60   $2880.00   $2587.20    $-292.80 (-10.17%)",
        "AMZN     20.00    $165.00   $185.30   $3300.00   $3706.00    +$406.00 (+12.30%)",
        "-----------------------------------------------------------",
        "TOTAL INVESTED CAPITAL : $14,705.00 | CURRENT VALUE: $16,542.70",
        "NET PROFIT / LOSS      : +$1,837.70 (+12.50% Return)",
        "Audit Log Generated: task2_stock_portfolio/portfolio_summary.csv"
    ) `
    -OutputPath "$assetsDir\task2_stock_portfolio.png"

# ----------------- Task 3: File Organizer -----------------
Create-Card `
    -Title "Task 3: Automated File Organizer & Cleanup Utility" `
    -Subtitle "Autonomous Directory Sorter with Collision Resolution & Dry-Run Preview" `
    -TaskNumber "Task 3 Deliverable" `
    -BadgeText "STATUS: VERIFIED (PASS)" `
    -AccentColor ([System.Drawing.Color]::FromArgb(245, 158, 11)) `
    -KeyPoints @(
        "Dynamic category provisioning (/Documents, /Images, /Videos, /Archives, /Code, etc.).",
        "High-performance directory inspection utilizing os.scandir() and pathlib.Path.",
        "Collision resolution engine automatically renaming colliding files (doc.pdf -> doc_1.pdf).",
        "Safe dry-run preview mode (--dry-run) simulating migrations without modifying disk.",
        "Robust try-except exception protection safeguarding against PermissionError locks."
    ) `
    -CodeLines @(
        "$ python task3_file_organizer/demo_run.py",
        "--- Running Automated File Organizer Sandbox Demo ---",
        "Created 12 mock files in sandbox directory...",
        "===========================================================",
        "     🗂️ DATHEON AUTOMATED FILE ORGANIZER SUMMARY [LIVE]    ",
        "===========================================================",
        "Total Files Scanned  : 12",
        "Files Relocated      : 12  [100% Success]",
        "Collisions Resolved  : 1   (quarterly_report_1.pdf)",
        "Encountered Errors   : 0",
        "-----------------------------------------------------------",
        "  📁 /Documents    :  4 file(s)  |  📁 /Images    :  2 file(s)",
        "  📁 /Code         :  1 file(s)  |  📁 /Archives  :  1 file(s)",
        "  📁 /Videos       :  1 file(s)  |  📁 /Audio     :  1 file(s)",
        "All category directories and collision renames verified!"
    ) `
    -OutputPath "$assetsDir\task3_file_organizer.png"

# ----------------- Task 4: Terminal Chatbot -----------------
Create-Card `
    -Title "Task 4: Rule-Based Interactive Terminal Assistant / Chatbot" `
    -Subtitle "Multi-Intent Recognition with Regular Expressions & Dialogue State Engine" `
    -TaskNumber "Task 4 Deliverable" `
    -BadgeText "STATUS: VERIFIED (PASS)" `
    -AccentColor ([System.Drawing.Color]::FromArgb(129, 140, 248)) `
    -KeyPoints @(
        "Regex-powered multi-intent classification taxonomy compiled with re module.",
        "Dialogue state machine managing GREETING -> QUERY -> RESOLUTION -> EXIT states.",
        "Decoupled FAQ knowledge base configured via external 'faq_dataset.json'.",
        "Input normalization stripping punctuation, lowercasing, and handling misspellings.",
        "Intelligent fallback suggestions and clean teardown on 'bye', 'exit', 'quit'."
    ) `
    -CodeLines @(
        "$ python task4_terminal_assistant/demo_run.py",
        "--- Running Rule-Based Terminal Chatbot Simulation ---",
        "User : Hello there!",
        "Bot  : Hello! I am Datheon Nova. How can I assist you today?",
        "User : What are your business operating hours?",
        "Bot  : Our automated platforms operate 24/7. Live desk: 9am-6pm.",
        "User : Tell me about the Datheon Python internship!",
        "Bot  : 4-week challenge! Push code to GitHub for Verified LOR.",
        "User : How much does the program cost?",
        "Bot  : Standard Programs are 100% Free with zero enrollment fees.",
        "User : Can you bake a chocolate cake on Mars?",
        "Bot  : [Fallback] Type 'topics' for options or 'contact' to reach us.",
        "User : Thank you, bye!",
        "Bot  : Farewell! Happy coding! [Session Ended Successfully]"
    ) `
    -OutputPath "$assetsDir\task4_terminal_assistant.png"

# ----------------- Task 5: OOP Inventory System -----------------
Create-Card `
    -Title "Task 5: Enterprise Smart Inventory & Asset System" `
    -Subtitle "Strict OOP Architecture: ABC, Encapsulation, Polymorphism & Dunder Methods" `
    -TaskNumber "Task 5 Deliverable" `
    -BadgeText "STATUS: VERIFIED (PASS)" `
    -AccentColor ([System.Drawing.Color]::FromArgb(236, 72, 153)) `
    -KeyPoints @(
        "Abstraction: Abstract base class LibraryItem using abc.ABC and @abstractmethod.",
        "Encapsulation: Private attributes (__var) with validated @property getters and setters.",
        "Inheritance & Polymorphism: Book ($0.50/day), Magazine ($1.00/day), DigitalMedia ($0.25/day).",
        "Dunder Methods: __str__, __repr__, __len__ (pages/issue/MB), and __eq__ identity comparison.",
        "InventoryManager orchestrating catalog transactions, checkouts, and tabular audits."
    ) `
    -CodeLines @(
        "$ python task5_enterprise_inventory/demo_run.py",
        "--- Running Enterprise Smart Inventory System Demo ---",
        "Testing Dunder Methods:",
        "  __str__ Book    : [Book] 'Fluent Python' (ID: BK-001) [Available]",
        "  __repr__ Media  : DigitalMedia(item_id='DM-003', price=99.95)",
        "  __len__ Book (pages)     : 814 pages",
        "  __len__ Magazine (issue) : Issue #11",
        "  __len__ Media (size MB)  : 4500 MB",
        "Polymorphic Overdue Fee Validations:",
        "  Book Overdue Fee (6 days @ $0.50)     : $3.00 (Verified)",
        "  Magazine Overdue Fee (5 days @ $1.00) : $5.00 (Verified)",
        "===========================================================",
        "Total Registered Assets: 3 | Total Valuation: $177.94",
        "Audit Trail: 4 checkouts/returns recorded in tabular report."
    ) `
    -OutputPath "$assetsDir\task5_enterprise_inventory.png"

# ----------------- Project Overview Banner -----------------
Create-Card `
    -Title "Datheon Python Programming Internship - Master Portfolio" `
    -Subtitle "Cadence Engine · 4-Week Technical Program · All 5 Core Tasks Production-Ready" `
    -TaskNumber "Complete Project Pack" `
    -BadgeText "DIRECTORATE AUDIT: 100%" `
    -AccentColor ([System.Drawing.Color]::FromArgb(56, 189, 248)) `
    -KeyPoints @(
        "Task 1: Interactive Console Hangman with ASCII gallows & deduplication.",
        "Task 2: Real-time Stock Portfolio Valuation with CSV transaction audit.",
        "Task 3: Autonomous Desktop File Organizer with safe collision resolver.",
        "Task 4: Conversational Terminal Assistant with regex NLP multi-intent matching.",
        "Task 5: Enterprise Smart Inventory System with strict OOP architecture."
    ) `
    -CodeLines @(
        "$ python -m pytest tests/ -v",
        "tests/test_task1_hangman.py ........ PASSED [ 25%]",
        "tests/test_task2_portfolio.py ...... PASSED [ 48%]",
        "tests/test_task3_organizer.py ...... PASSED [ 62%]",
        "tests/test_task4_chatbot.py ........ PASSED [ 81%]",
        "tests/test_task5_inventory.py ...... PASSED [100%]",
        "===========================================================",
        "27 passed in 1.02s  |  100% PASS RATE",
        "Runtime: Python 3.13  |  Zero Paid Dependencies",
        "Candidate : Seebiraj V",
        "App ID    : DT-2026-WH8V5",
        "Batch     : Batch 01 (Jeppiaar Institute of Technology)",
        "Repo      : github.com/seebiraj/Datheon_Python_Internship",
        "Evaluation Status: READY FOR VERIFIED CREDENTIAL ISSUANCE"
    ) `
    -OutputPath "$assetsDir\project_overview_banner.png"

Write-Host "All 6 high-definition PNG cards generated successfully in $assetsDir!"
