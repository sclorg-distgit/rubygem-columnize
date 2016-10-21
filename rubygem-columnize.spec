%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name columnize

Summary:        Module to format an Array as an Array of String aligned in columns
Name:           %{?scl_prefix}rubygem-%{gem_name}
Version:        0.8.9
Release:        4%{?dist}
Group:          Development/Languages
License:        Ruby or GPLv2
URL:            https://github.com/rocky/columnize
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:       %{?scl_prefix_ruby}ruby(release)
Requires:       %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires:  %{?scl_prefix_ruby}ruby(release)
BuildRequires:  %{?scl_prefix_ruby}rubygems-devel
BuildRequires:  %{?scl_prefix_ruby}rubygem(minitest)
BuildArch:      noarch
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
In showing a long lists, sometimes one would prefer to see the value
arranged aligned in columns. Some examples include listing methods
of an object or debugger commands.
See Examples in the rdoc documentation for examples.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%{?scl:scl enable %{scl} - << \EOF}
set -e
pushd .%{gem_instdir}
ruby -rminitest/autorun - << \EOR
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end
  end

  Test = Minitest

  Dir.glob "./test/test-*.rb", &method(:require)
EOR
popd
%{?scl:EOF}

%files
%doc %{gem_instdir}/COPYING
%doc %{gem_docdir}/
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}/
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/AUTHORS
%doc %{gem_instdir}/ChangeLog
%{gem_instdir}/columnize.gemspec
%{gem_instdir}/Gemfile*
%{gem_instdir}/Makefile
%doc %{gem_instdir}/NEWS
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/THANKS
%{gem_instdir}/test/

%changelog
* Wed Apr 06 2016 Pavel Valena <pvalena@redhat.com> - 0.8.9-4
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 08 2014 Vít Ondruch <vondruch@redhat.com> - 0.8.9-1
- Update to columnize 0.8.9.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.1-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.3.1-6
- F-17: rebuild against ruby19

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 14 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3.1-3
- Enable %%check

* Wed Oct 21 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3.1-2
- Fix license

* Wed Oct 14 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3.1-1
- First package
