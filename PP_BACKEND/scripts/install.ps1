# ============================================================================
# Script d'installation pour Windows - DZ CarPool Backend
# Usage: .\scripts\install.ps1
# ============================================================================

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Installation des dépendances DZ CarPool Backend" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier Python
Write-Host "Vérification de Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR: Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Mettre à jour pip
Write-Host ""
Write-Host "Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# Installer les dépendances critiques en premier
Write-Host ""
Write-Host "Installation des dépendances critiques..." -ForegroundColor Yellow

$criticalPackages = @(
    "Django==4.2.11",
    "djangorestframework==3.14.0",
    "python-decouple==3.8",
    "psycopg2-binary==2.9.9"
)

foreach ($package in $criticalPackages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    pip install $package
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERREUR lors de l'installation de $package" -ForegroundColor Red
    }
}

# Installer Pillow avec une version compatible
Write-Host ""
Write-Host "Installation de Pillow (traitement d'images)..." -ForegroundColor Yellow
pip install --upgrade Pillow
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ATTENTION: Pillow n'a pas pu être installé" -ForegroundColor Yellow
    Write-Host "  Le projet fonctionnera mais sans traitement d'images" -ForegroundColor Yellow
}

# Installer le reste des dépendances
Write-Host ""
Write-Host "Installation des autres dépendances..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Certaines dépendances ont échoué" -ForegroundColor Yellow
    Write-Host "  Continuons quand même..." -ForegroundColor Yellow
}

# Vérifier l'installation
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Vérification de l'installation" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

$packagesToCheck = @(
    "django",
    "rest_framework",
    "corsheaders",
    "decouple",
    "psycopg2"
)

$allInstalled = $true
foreach ($package in $packagesToCheck) {
    python -c "import $package" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $package" -ForegroundColor Green
    } else {
        Write-Host "✗ $package - MANQUANT" -ForegroundColor Red
        $allInstalled = $false
    }
}

Write-Host ""
if ($allInstalled) {
    Write-Host "✅ Installation réussie!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Certains packages sont manquants" -ForegroundColor Yellow
    Write-Host "   Vous pouvez réessayer avec: pip install -r requirements.txt" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Prochaines étapes:" -ForegroundColor Cyan
Write-Host "  1. Créer le fichier .env: copy .env.example .env" -ForegroundColor Gray
Write-Host "  2. Configurer la base de données dans .env" -ForegroundColor Gray
Write-Host "  3. Lancer les migrations: python manage.py migrate" -ForegroundColor Gray
Write-Host "  4. Démarrer le serveur: python manage.py runserver" -ForegroundColor Gray