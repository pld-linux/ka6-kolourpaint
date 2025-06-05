#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.2
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kolourpaint
Summary:	kolourpaint
Name:		ka6-%{kaname}
Version:	25.04.2
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	5ae6c02e345a102f760d894184b77fdf
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-libksane-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-ktextwidgets-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KolourPaint is a simple painting program to quickly create raster
images. It is useful as a touch-up tool and simple image editing
tasks.

Features: Support for drawing various shapes - lines, rectangles,
rounded rectangles, ovals and polygons.

%description -l pl.UTF-8
KolourPaint jest prostym programem do szybkiego tworzenia
rastrowych obrazków. Jest przydatny do retuszowania i prostych
zadań edycji obrazków.

Właściwości: Wsparcie dla rysowania różnych kształtów - linii,
prostokątów, zaokrąglonych prostokątów, owali i wieloboków.

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname}-data < %{version}
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/tok

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun

%files 
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kolourpaint
%{_libdir}/libkolourpaint_lgpl.so
%attr(755,root,root) %{_libdir}/libkolourpaint_lgpl.so.5

%files data -f %{kaname}.lang
%{_desktopdir}/org.kde.kolourpaint.desktop
%{_iconsdir}/hicolor/*x*/apps/kolourpaint.png
%{_iconsdir}/hicolor/scalable/apps/kolourpaint.svgz
%{_datadir}/kolourpaint
%{_datadir}/metainfo/org.kde.kolourpaint.appdata.xml
